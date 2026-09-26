"""Response-grain robustness re-runs for the corrected draft (v2).
Mirrors the original methodologies but at the response grain (unit = response,
ratings averaged within response), using recompute/response_level.csv (frozen).

Outputs: recompute/robustness_response.csv(s) + printed log.
"""
import numpy as np
import pandas as pd
from scipy import stats
from math import sqrt
from sklearn.ensemble import IsolationForest

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # repo root
OUT = ROOT / "results" / "response_grain"
resp = pd.read_csv(OUT / "response_level.csv")
DIMS = ["Novelty", "Usefulness", "Flexibility", "Elaboration", "Cultural Sensitivity"]
PERSONAS = ["Culture_5", "Culture_Expert", "Culture_11"]
CONDS4 = PERSONAS + ["Large_Baseline"]
FAMS = ["Claude", "DeepSeek", "GPT", "Llama", "Mistral", "Qwen", "Gemini"]

def cohens_d(a, b):
    a, b = pd.Series(a).dropna(), pd.Series(b).dropna()
    n1, n2 = len(a), len(b)
    sp = sqrt(((n1-1)*a.std()**2 + (n2-1)*b.std()**2) / (n1+n2-2))
    return (a.mean() - b.mean()) / sp if sp else 0.0

sub = resp[resp.condition.isin(CONDS4)]

print("="*70)
print("B1. LEAVE-ONE-OUT (response grain; method of leave_one.py)")
print("="*70)
orig = {}
for p in PERSONAS:
    ds = [cohens_d(sub[(sub.family==f)&(sub.condition==p)]["Novelty"],
                   sub[(sub.family==f)&(sub.condition=="Large_Baseline")]["Novelty"]) for f in FAMS]
    orig[p] = np.mean(ds)
rows = []
for rem in FAMS:
    keep = [f for f in FAMS if f != rem]
    for p in PERSONAS:
        ds = [cohens_d(sub[(sub.family==f)&(sub.condition==p)]["Novelty"],
                       sub[(sub.family==f)&(sub.condition=="Large_Baseline")]["Novelty"]) for f in keep]
        rows.append({"removed": rem, "persona": p, "avg_d_loo": np.mean(ds),
                     "avg_d_orig": orig[p], "change": np.mean(ds)-orig[p]})
loo = pd.DataFrame(rows)
loo["abs"] = loo.change.abs()
summ = loo.groupby("removed")["abs"].mean().sort_values(ascending=False)
print(summ.round(4).to_string())
print(f"mean|Delta| {loo['abs'].mean():.4f}  max {loo['abs'].max():.4f}  "
      f"frac<0.1 {(loo['abs']<0.1).mean()*100:.1f}%")
loo.to_csv(f"{OUT}/loo_response.csv", index=False)
summ.to_csv(f"{OUT}/loo_summary_response.csv")

print("="*70)
print("B2. TRAIN-TEST SPLIT 80/20 by problem (response grain, seed 42)")
print("="*70)
rng = np.random.default_rng(42)
probs = np.sort(sub.problem_id.unique())
rng.shuffle(probs)
train_p, test_p = probs[:80], probs[80:]
tt = []
for p in PERSONAS:
    out = {"persona": p}
    for label, P in [("train", train_p), ("test", test_p)]:
        s = sub[sub.problem_id.isin(P)]
        d = cohens_d(s[s.condition==p]["Novelty"], s[s.condition=="Large_Baseline"]["Novelty"])
        out[f"d_{label}"] = round(d, 3)
    out["delta"] = round(out["d_test"] - out["d_train"], 3)
    tt.append(out)
tt = pd.DataFrame(tt)
print(tt.to_string(index=False))
tt.to_csv(f"{OUT}/train_test_response.csv", index=False)

print("="*70)
print("B3. MEAN vs MEDIAN (response grain, model x condition cells)")
print("="*70)
cells = sub.groupby(["family", "condition"])["Novelty"].agg(["mean", "median"])
r, pval = stats.pearsonr(cells["mean"], cells["median"])
diff = cells["mean"] - cells["median"]
print(f"r = {r:.4f} (p {pval:.2e}); mean-median diff range {diff.min():.3f} to {diff.max():.3f}; n cells {len(cells)}")
cells.to_csv(f"{OUT}/mean_median_response.csv")

print("="*70)
print("B4. ISOLATION FOREST (response grain, 5 dims, contamination 0.1)")
print("="*70)
X = sub[DIMS].dropna()
iso = IsolationForest(contamination=0.1, random_state=42)
flags = iso.fit_predict(X)
frac = (flags == -1).mean()
print(f"flagged outliers: {(flags==-1).sum()} / {len(X)} = {frac*100:.1f}%")
keep_mask = pd.Series(flags == 1, index=X.index)
d_all = {p: cohens_d(sub.loc[X.index][keep_mask][lambda d: d.condition==p]["Novelty"],
                     sub.loc[X.index][keep_mask][lambda d: d.condition=="Large_Baseline"]["Novelty"]) for p in PERSONAS}
d_full = {p: cohens_d(sub[sub.condition==p]["Novelty"], sub[sub.condition=="Large_Baseline"]["Novelty"]) for p in PERSONAS}
for p in PERSONAS:
    print(f"  {p}: full d {d_full[p]:.3f} -> without outliers {d_all[p]:.3f} (delta {d_all[p]-d_full[p]:+.3f})")

print("="*70)
print("B5. ANOVA ASSUMPTIONS (response grain)")
print("="*70)
from statsmodels.formula.api import ols
s2 = sub.dropna(subset=["Novelty"]).copy()
s2["persona4"] = s2["condition"]
fit = ols("Novelty ~ C(persona4, Sum)*C(region, Sum)", data=s2).fit()
W, p_sh = stats.shapiro(fit.resid[:5000])
lev = stats.levene(*[g["Novelty"].values for _, g in s2.groupby("persona4")])
print(f"Shapiro-Wilk W={W:.4f} p={p_sh:.3e}; Levene stat={lev.statistic:.3f} p={lev.pvalue:.3e}")

print("="*70)
print("B6. GPT Culture_5 100-problem sensitivity (response grain)")
print("="*70)
gpt = resp[(resp.family=="GPT")]
all_probs = set(resp.problem_id.unique())
gpt_c5_probs = set(gpt[gpt.condition=="Culture_5"].problem_id.unique())
common = all_probs  # problems 0..99
extra = gpt_c5_probs - common
print(f"GPT C5 problems: {len(gpt_c5_probs)}, outside 0-99: {sorted(extra)}")
a_full = gpt[(gpt.condition=="Culture_5")]["Novelty"].dropna()
a_100 = gpt[(gpt.condition=="Culture_5") & (gpt.problem_id.isin(common))]["Novelty"].dropna()
b = gpt[gpt.condition=="Large_Baseline"]["Novelty"].dropna()
print(f"d full (n={len(a_full)}): {cohens_d(a_full, b):.3f}; d 100-problem (n={len(a_100)}): {cohens_d(a_100, b):.3f}")

print("="*70)
print("B7. Table 16 baseline identity (other dims, rating grain means)")
print("="*70)
df = pd.read_csv(ROOT / "data" / "unified_evaluations.csv", low_memory=False)
df.columns = [c.strip() for c in df.columns]
fam_map = {"claude-sonnet-4-6": "Claude", "claude-opus-4-6": "Claude",
           "gpt-5-mini-2025-08-07": "GPT", "gpt-5.4-2026-03-05": "GPT",
           "Meta-Llama-3.1-8B-Instruct-Turbo": "Llama", "Llama-3.3-70B-Instruct-Turbo": "Llama",
           "Mixtral-8x7B-Instruct-v0.1": "Mistral", "Mistral-Small-24B-Instruct-2501": "Mistral",
           "gemini-3.1-flash-lite-preview": "Gemini", "gemini-3.1-pro-preview": "Gemini",
           "deepseek-chat": "DeepSeek", "deepseek-reasoner": "DeepSeek",
           "Qwen2.5-7B-Instruct-Turbo": "Qwen", "Qwen3-Next-80B-A3B-Instruct": "Qwen"}
df["family"] = df["LLM evaluated"].map(fam_map)
for fam in ["Claude", "DeepSeek", "GPT", "Gemini"]:
    for cond in ["Small_Baseline", "Large_Baseline"]:
        m = df[(df.family==fam)&(df.condition==cond)][DIMS[1:]].mean().round(2).tolist()
        print(f"  {fam} {cond}: {m}")
print("DONE")
