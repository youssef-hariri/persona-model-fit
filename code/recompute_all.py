"""Response-level recomputation for 'Doing More with Less' (audit + corrections).

Protocol
  source   : repo export data/unified_evaluations.csv (judge/variation columns complete;
             local fixed file has misaligned custom_id + empty judge cols for openai/gemini)
  rating   : one row per (judge x prompt_variation) score  <- grain of paper tables
  response : one row per (model, condition, problem_id, copy); ratings averaged;
             groups with >9 ratings split into copies via duplicate (judge, vark) index
  NaN      : parse-failure ratings dropped per dimension
"""
import re
import os
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.power import TTestIndPower

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # repo root
REPO = ROOT / "data" / "unified_evaluations.csv"    # released evaluation data
OUT = ROOT / "results" / "response_grain"           # frozen outputs of this pipeline
os.makedirs(OUT, exist_ok=True)

DIMS = ["Novelty", "Usefulness", "Flexibility", "Elaboration", "Cultural Sensitivity"]
PERSONAS = ["Culture_5", "Culture_Expert", "Culture_11"]
FAM_DISPLAY = {"claude": "Claude", "openai": "GPT", "llama": "Llama", "mistral": "Mistral",
               "gemini": "Gemini", "deepseek": "DeepSeek", "qwen": "Qwen"}
REGION = {"Claude": "Western", "GPT": "Western", "Llama": "Western", "Mistral": "Western",
          "Gemini": "Western", "DeepSeek": "Eastern", "Qwen": "Eastern"}
COST = {"GPT": (2.0, 15.0), "Claude": (15.0, 25.0), "DeepSeek": (0.42, 0.42),
        "Llama": (0.20, 0.88), "Mistral": (0.60, 0.30), "Qwen": (0.30, 1.50),
        "Gemini": (1.50, 12.0)}
FAMS = ["Claude", "DeepSeek", "GPT", "Llama", "Mistral", "Qwen", "Gemini"]


def vark(cid):
    m = re.search(r"_var(\d)_", cid)
    return m.group(1) if m else None


df = pd.read_csv(REPO)
df.columns = [c.strip() for c in df.columns]
df = df.rename(columns={"LLM evaluated": "model", "prompt_variation": "var_col"})
df["vark"] = df["custom_id"].map(vark)
df["problem_id"] = df["problem_id"].astype(int)
df["family"] = df["model"].map(
    lambda x: {"claude-sonnet-4-6": "Claude", "claude-opus-4-6": "Claude",
               "gpt-5-mini-2025-08-07": "GPT", "gpt-5.4-2026-03-05": "GPT",
               "Meta-Llama-3.1-8B-Instruct-Turbo": "Llama", "Llama-3.3-70B-Instruct-Turbo": "Llama",
               "Mixtral-8x7B-Instruct-v0.1": "Mistral", "Mistral-Small-24B-Instruct-2501": "Mistral",
               "gemini-3.1-flash-lite-preview": "Gemini", "gemini-3.1-pro-preview": "Gemini",
               "deepseek-chat": "DeepSeek", "deepseek-reasoner": "DeepSeek",
               "Qwen2.5-7B-Instruct-Turbo": "Qwen", "Qwen3-Next-80B-A3B-Instruct": "Qwen"}[x])
df["region"] = df["family"].map(REGION)
df["domain"] = df["problem_id"].map(
    lambda p: "Reasoning" if p <= 24 else "Instruction" if p <= 49
    else "Creative" if p <= 74 else "GeneralKnowledge")

# un-merge responses that share (model, condition, problem_id) with >9 ratings
grp = df.groupby(["family", "condition", "problem_id"])
sizes = grp["Novelty"].transform("size")
df["copy"] = 0
mask = sizes > 9
df.loc[mask, "copy"] = (df.loc[mask].groupby(["family", "condition", "problem_id", "judge", "vark"])
                        .cumcount())
print("R2 rows", len(df), "merged-response rows split:", int(mask.sum()),
      "responses:", df.groupby(["family", "condition", "problem_id", "copy"]).ngroups)

resp = df.groupby(["family", "region", "condition", "problem_id", "copy"], as_index=False)[DIMS].mean()
resp["domain"] = resp["problem_id"].map(
    lambda p: "Reasoning" if p <= 24 else "Instruction" if p <= 49
    else "Creative" if p <= 74 else "GeneralKnowledge")
resp["n_ratings"] = df.groupby(["family", "condition", "problem_id", "copy"]).size().values
resp.to_csv(f"{OUT}/response_level.csv", index=False)


def cohens_d(a, b):
    n1, n2 = len(a), len(b)
    sp = np.sqrt(((n1 - 1) * a.var(ddof=1) + (n2 - 1) * b.var(ddof=1)) / (n1 + n2 - 2))
    return (a.mean() - b.mean()) / sp


def boot_ci(a, b, iters=5000, seed=42):
    rng = np.random.default_rng(seed)
    n1, n2 = len(a), len(b)
    ds = np.empty(iters)
    for i in range(iters):
        ds[i] = cohens_d(a[rng.integers(0, n1, n1)], b[rng.integers(0, n2, n2)])
    return np.percentile(ds, [2.5, 97.5])


def effect_table(frame, label):
    rows = []
    for fam in FAMS:
        base = frame[(frame.family == fam) & (frame.condition == "Large_Baseline")]["Novelty"].dropna().to_numpy()
        for p in PERSONAS:
            a = frame[(frame.family == fam) & (frame.condition == p)]["Novelty"].dropna().to_numpy()
            d = cohens_d(a, base)
            lo, hi = boot_ci(a, base)
            rows.append((fam, p, round(d, 3), round(lo, 3), round(hi, 3), len(a), len(base)))
    t = pd.DataFrame(rows, columns=["model", "persona", "d", "ci_lo", "ci_hi", "n1", "n2"])
    t["sig"] = ~((t.ci_lo <= 0) & (t.ci_hi >= 0))
    t.to_csv(f"{OUT}/effect_sizes_{label}.csv", index=False)
    return t


print("R3 DESCRIPTIVES response-level (means / SDs / n responses)")
g = resp.groupby(["family", "condition"])["Novelty"].agg(n="size", mean="mean", sd="std")
print(g["mean"].unstack("condition")[PERSONAS + ["Large_Baseline"]].round(2).to_string())
print(g["sd"].unstack("condition")[PERSONAS + ["Large_Baseline"]].round(2).to_string())
print(g["n"].unstack("condition")[PERSONAS + ["Large_Baseline"]].to_string())
g.round(4).to_csv(f"{OUT}/descriptives_response.csv")
gr = df.groupby(["family", "condition"])["Novelty"].agg(n="size", mean="mean", sd="std")
print("R3b DESCRIPTIVES rating-level (paper grain)")
print(gr["mean"].unstack("condition")[PERSONAS + ["Large_Baseline"]].round(2).to_string())
print(gr["n"].unstack("condition")[PERSONAS + ["Large_Baseline"]].to_string())
gr.round(4).to_csv(f"{OUT}/descriptives_rating.csv")

print("R4 EFFECT SIZES rating-level (validate vs paper Table 3)")
tr = effect_table(df, "rating")
print(tr.to_string(index=False))
print("R4b EFFECT SIZES response-level (corrected)")
ts = effect_table(resp, "response")
print(ts.to_string(index=False))

print("R5 TWO-WAY ANOVA persona(4) x region(2)")
for frame, label in [(df, "rating"), (resp, "response")]:
    sub = frame[frame.condition.isin(PERSONAS + ["Large_Baseline"])].dropna(subset=["Novelty"]).copy()
    sub["persona4"] = sub["condition"]
    fit = ols("Novelty ~ C(persona4, Sum)*C(region, Sum)", data=sub).fit()
    aov = anova_lm(fit, typ=2)
    print(f"  [{label}] n={len(sub)}")
    print(aov.round(4).to_string())
    aov.round(4).to_csv(f"{OUT}/anova_{label}.csv")

print("R6 MODERATION SPECS")
for frame, label in [(df, "rating"), (resp, "response")]:
    sub = frame[frame.condition.isin(PERSONAS + ["Large_Baseline"])].dropna(subset=["Novelty"]).copy()
    sub["IsEastern"] = (sub.region == "Eastern").astype(int)
    sub["IsPersona"] = (sub.condition != "Large_Baseline").astype(int)
    fit = ols("Novelty ~ IsEastern*IsPersona", data=sub).fit()
    print(f"  [{label}] binary persona-vs-LB")
    print(pd.DataFrame({"coef": fit.params.round(4), "t": fit.tvalues.round(3),
                        "p": fit.pvalues.round(4)}).to_string())
    pd.DataFrame({"coef": fit.params, "SE": fit.bse, "t": fit.tvalues,
                  "p": fit.pvalues}).round(4).to_csv(f"{OUT}/moderation_{label}.csv")
    sub2 = frame[frame.condition.isin(PERSONAS)].dropna(subset=["Novelty"]).copy()
    sub2["IsEastern"] = (sub2.region == "Eastern").astype(int)
    fit2 = ols("Novelty ~ C(condition, Treatment('Culture_11'))*IsEastern", data=sub2).fit()
    print(f"  [{label}] persona C() x East (ref Culture_11)")
    print(pd.DataFrame({"coef": fit2.params.round(4), "t": fit2.tvalues.round(3),
                        "p": fit2.pvalues.round(4)}).to_string())
    fit3 = ols("Novelty ~ C(condition, Treatment('Culture_11'))*IsEastern", data=sub2).fit(cov_type="HC3")
    print(f"  [{label}] same, HC3 robust SE: interaction t/p:")
    for nm in fit3.params.index:
        if ":IsEastern" in nm:
            print("   ", nm, round(fit3.tvalues[nm], 3), round(fit3.pvalues[nm], 4))

print("R7 FLEISS KAPPA")


def fleiss_kappa(mat):
    mat = np.asarray(mat, float)
    n = mat.sum(axis=1)[0]
    P_i = ((mat ** 2).sum(axis=1) - n) / (n * (n - 1))
    p_k = mat.sum(axis=0) / mat.sum()
    Pe = (p_k ** 2).sum()
    return (P_i.mean() - Pe) / (1 - Pe)


rows = []
for dim in DIMS:
    sub = df[df.condition.isin(PERSONAS + ["Large_Baseline"])].dropna(subset=[dim])
    g9 = sub.groupby(["family", "condition", "problem_id", "copy"])[dim].apply(list)
    mat = np.zeros((len(g9), 5))
    for i, vals in enumerate(g9):
        for v in vals:
            mat[i, int(v) - 1] += 1
    gj = sub.groupby(["family", "condition", "problem_id", "copy", "judge"])[dim].mean()
    gj = gj.groupby(level=[0, 1, 2, 3]).apply(list)
    mat3 = np.zeros((len(gj), 5))
    for i, vals in enumerate(gj):
        for v in vals:
            mat3[i, min(4, max(0, int(round(v)) - 1))] += 1
    rows.append((dim, round(fleiss_kappa(mat), 3), round(fleiss_kappa(mat[:35]), 3),
                 round(fleiss_kappa(mat3), 3)))
kt = pd.DataFrame(rows, columns=["dimension", "kappa_9raters_all", "kappa_9raters_first35",
                                 "kappa_3judgerounds_all"])
print(kt.to_string(index=False))
kt.to_csv(f"{OUT}/fleiss_kappa.csv", index=False)

print("R8 POST-HOC POWER")
for label, t in [("rating", tr), ("response", ts)]:
    pw = [TTestIndPower().solve_power(effect_size=abs(r.d), nobs1=r.n1, ratio=r.n2 / r.n1, alpha=0.05)
          for _, r in t.iterrows()]
    t = t.assign(power=np.round(pw, 3))
    print(f"  [{label}] mean power {round(t.power.mean(), 3)} frac>=.8 {round((t.power >= .8).mean(), 3)}")
    t.to_csv(f"{OUT}/power_{label}.csv", index=False)

print("R9 PURE PERSONA EFFECTS vs Small_Baseline + BH-FDR")
for label, frame in [("rating", df), ("response", resp)]:
    rows, ps = [], []
    for fam in FAMS:
        sb = frame[(frame.family == fam) & (frame.condition == "Small_Baseline")]["Novelty"].dropna().to_numpy()
        for p in PERSONAS:
            a = frame[(frame.family == fam) & (frame.condition == p)]["Novelty"].dropna().to_numpy()
            tt, pv = stats.ttest_ind(a, sb, equal_var=False)
            rows.append((fam, p, round(sb.mean(), 2), round(a.mean(), 2), round(cohens_d(a, sb), 3), pv))
            ps.append(pv)
    rej, q, _, _ = multipletests(ps, method="fdr_bh")
    pt = pd.DataFrame(rows, columns=["model", "persona", "base_mean", "persona_mean", "d", "p"])
    pt["p_fdr"] = np.round(q, 4)
    pt["star"] = ["*" if x else "" for x in rej]
    print(f"  [{label}]")
    print(pt.to_string(index=False))
    pt.to_csv(f"{OUT}/pure_persona_fdr_{label}.csv", index=False)

print("R10 DOMAIN EFFECT SIZES (pooled models)")
rows = []
for p in PERSONAS:
    for dname in ["Creative", "GeneralKnowledge", "Instruction", "Reasoning"]:
        out = [p, dname]
        for label, frame in [("resp", resp), ("rating", df)]:
            a = frame[(frame.condition == p) & (frame.domain == dname)]["Novelty"].dropna().to_numpy()
            b = frame[(frame.condition == "Large_Baseline") & (frame.domain == dname)]["Novelty"].dropna().to_numpy()
            out.append(round(cohens_d(a, b), 3))
        a = resp[(resp.condition == p) & (resp.domain == dname) & (resp.family != "Gemini")]["Novelty"].dropna().to_numpy()
        b = resp[(resp.condition == "Large_Baseline") & (resp.domain == dname) & (resp.family != "Gemini")]["Novelty"].dropna().to_numpy()
        out.append(round(cohens_d(a, b), 3))
        rows.append(out)
dt = pd.DataFrame(rows, columns=["persona", "domain", "d_response", "d_rating", "d_response_noGemini"])
print(dt.to_string(index=False))
dt.to_csv(f"{OUT}/domain_effects.csv", index=False)

print("R11 EGR + INCLUSION")
means_r = resp.groupby(["family", "condition"])["Novelty"].mean()
means_g = df.groupby(["family", "condition"])["Novelty"].mean()
rows = []
for fam in FAMS:
    cs, cl = COST[fam]
    for p in PERSONAS:
        dr = ts[(ts.model == fam) & (ts.persona == p)].iloc[0]
        egr = (means_r[(fam, p)] / means_r[(fam, "Large_Baseline")]) / (cs / cl)
        rows.append((fam, p, round(dr.d, 3), bool(dr.sig), round(1 - cs / cl, 3), round(egr, 2),
                     round(means_r[(fam, p)], 2), round(means_g[(fam, p)], 2)))
et = pd.DataFrame(rows, columns=["model", "persona", "d_resp", "ci_sig", "cost_savings",
                                 "EGR", "mean_resp", "mean_rating"])
print(et.to_string(index=False))
et.to_csv(f"{OUT}/egr_inclusion.csv", index=False)

print("R12 CLAIM CHECKS (response level)")
lb = resp.pivot_table(index="family", columns="condition", values="Novelty")
imp = lb[PERSONAS].sub(lb["Large_Baseline"], axis=0)
print("  point gains over LB:")
print(imp.round(3).to_string())
print("  pct gains:")
print((imp.div(lb["Large_Baseline"], axis=0) * 100).round(1).to_string())
print("  per-condition argmax:")
print(lb[PERSONAS + ["Large_Baseline"]].idxmax().to_string())
print("  Claude overall mean:", round(resp[resp.family == "Claude"]["Novelty"].mean(), 3),
      " Claude overall SD:", round(resp[resp.family == "Claude"]["Novelty"].std(), 3))
print("DONE")
