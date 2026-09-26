"""Regenerate all paper figures at the response grain (corrected v2).
Input: recompute/response_level.csv + recompute CSVs. Output: figures_v2/*.png
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from scipy import stats
from math import sqrt

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # repo root
FIG = ROOT / "paper" / "figures_v2"
import os; os.makedirs(FIG, exist_ok=True)

resp = pd.read_csv(ROOT / "results" / "response_grain" / "response_level.csv")
eff = pd.read_csv(ROOT / "results" / "response_grain" / "effect_sizes_response.csv")
dom = pd.read_csv(ROOT / "results" / "response_grain" / "domain_effects.csv")
PERSONAS = ["Culture_5", "Culture_Expert", "Culture_11"]
CONDS4 = PERSONAS + ["Large_Baseline"]
FAM_ORDER = ["DeepSeek", "Qwen", "Claude", "Gemini", "GPT", "Llama", "Mistral"]
EASTERN = {"DeepSeek", "Qwen"}
COND_COLORS = {"Culture_5": "#4c86b0", "Culture_Expert": "#b05a8a",
               "Culture_11": "#e8a33d", "Large_Baseline": "#7dab87"}
COND_LABELS = {"Culture_5": "Culture_5", "Culture_Expert": "Culture_Expert",
               "Culture_11": "Culture_11", "Large_Baseline": "Large Baseline"}

# ---------------- Figure 1: barplot ----------------
g = resp[resp.condition.isin(CONDS4)].groupby(["family", "condition"])["Novelty"].agg(["mean", "std"])
fig, ax = plt.subplots(figsize=(14, 7))
x = np.arange(len(FAM_ORDER)); w = 0.2
for i, c in enumerate(CONDS4):
    means = [g.loc[(f, c), "mean"] for f in FAM_ORDER]
    sds = [g.loc[(f, c), "std"] for f in FAM_ORDER]
    ax.bar(x + (i - 1.5) * w, means, w, yerr=sds, capsize=3,
           color=COND_COLORS[c], label=COND_LABELS[c], edgecolor="white")
ax.axvline(1.5, color="gray", ls=":", lw=1.5)
ax.text(0.5, 5.15, "EASTERN", ha="center", fontsize=13, color="#c0504d", fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#c0504d"))
ax.text(4.5, 5.15, "WESTERN", ha="center", fontsize=13, color="#4c86b0", fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#4c86b0"))
ax.set_xticks(x); ax.set_xticklabels(FAM_ORDER, fontsize=13)
ax.set_ylabel("Mean Novelty Score (1-5)", fontsize=13)
ax.set_xlabel("Model", fontsize=13)
ax.set_title("Mean Novelty Scores by Model and Condition", fontsize=16, fontweight="bold")
ax.set_ylim(0, 5.6); ax.legend(fontsize=11)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout(); plt.savefig(f"{FIG}/figure1_performance_barplot_novelty.png", dpi=160); plt.close()

# ---------------- Figure 2: forest plot ----------------
order = [(m, p) for m in ["Claude", "DeepSeek", "GPT", "Llama", "Mistral", "Qwen", "Gemini"] for p in PERSONAS]
d = eff.set_index(["model", "persona"])
fig, ax = plt.subplots(figsize=(10, 10))
ys = np.arange(len(order))[::-1]
for y, (m, p) in zip(ys, order):
    r = d.loc[(m, p)]
    col = "#c0504d" if m in EASTERN else "#4c86b0"
    ax.plot([r.ci_lo, r.ci_hi], [y, y], color=col, lw=2)
    ax.scatter([r.d], [y], color=col, s=80, zorder=3,
               edgecolor="black" if r.sig else col,
               marker="o" if r.sig else "x")
ax.axvline(0, color="gray", ls="--", lw=1.2)
ax.set_yticks(ys); ax.set_yticklabels([f"{m} - {p}" for m, p in order], fontsize=10)
ax.set_xlabel("Cohen's d (95% bootstrap CI)", fontsize=12)
ax.set_title("Persona Effects on Novelty vs Large Baseline (response level)", fontsize=14, fontweight="bold")
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([0], [0], marker="o", color="w", markerfacecolor="#c0504d", markersize=10, label="Eastern"),
                   Line2D([0], [0], marker="o", color="w", markerfacecolor="#4c86b0", markersize=10, label="Western"),
                   Line2D([0], [0], marker="x", color="gray", markersize=10, label="CI includes 0 (n.s.)")],
          fontsize=10, loc="lower right")
ax.grid(axis="x", alpha=0.3)
plt.tight_layout(); plt.savefig(f"{FIG}/figure2_forest_plot_novelty.png", dpi=160); plt.close()

# ---------------- Figure 3: domain heatmap ----------------
piv = dom.pivot_table(index="persona", columns="domain", values="d_response")
piv = piv.loc[PERSONAS, ["Creative", "GeneralKnowledge", "Instruction", "Reasoning"]]
fig, ax = plt.subplots(figsize=(11, 4.5))
im = ax.imshow(piv.values, cmap="RdBu_r", vmin=-0.7, vmax=0.7, aspect="auto")
ax.set_xticks(range(4)); ax.set_xticklabels(["Creative", "General Knowledge", "Instruction", "Reasoning"], fontsize=12)
ax.set_yticks(range(3)); ax.set_yticklabels(PERSONAS, fontsize=12)
for i in range(3):
    for j in range(4):
        v = piv.values[i, j]
        ax.text(j, i, f"{v:.3f}", ha="center", va="center", fontsize=13, fontweight="bold",
                color="white" if abs(v) > 0.45 else "black")
ax.set_title("Effect Sizes for Novelty by Persona and Domain (response level)", fontsize=14, fontweight="bold")
ax.set_xlabel("Domain", fontsize=12); ax.set_ylabel("Persona", fontsize=12)
plt.colorbar(im, label="Cohen's d")
plt.tight_layout(); plt.savefig(f"{FIG}/figure3_domain_heatmap_novelty.png", dpi=160); plt.close()

# ---------------- Figure 4: MDS ----------------
prof = resp[resp.condition.isin(CONDS4)].groupby(["family", "condition"])["Novelty"].mean().unstack()
prof = prof[CONDS4]
mds = MDS(n_components=2, random_state=42, dissimilarity="euclidean")
xy = mds.fit_transform(prof.values)
fig, ax = plt.subplots(figsize=(9, 8))
LABEL_OFFSETS = {"Llama": (16, 12), "Mistral": (16, -24)}  # these two points nearly coincide
for (fam, _), (xx, yy) in zip(prof.iterrows(), xy):
    col = "#c0504d" if fam in EASTERN else "#4c86b0"
    ax.scatter([xx], [yy], s=350, color=col, edgecolor="black", zorder=3, alpha=0.85)
    dx, dy = LABEL_OFFSETS.get(fam, (12, 8))
    ax.annotate(fam, (xx, yy), textcoords="offset points", xytext=(dx, dy), fontsize=13, fontweight="bold")
ax.axhline(0, color="gray", ls="--", lw=1); ax.axvline(0, color="gray", ls="--", lw=1)
ax.set_xlabel("MDS Dimension 1", fontsize=12); ax.set_ylabel("MDS Dimension 2", fontsize=12)
ax.set_title("Model Clustering Based on Novelty Performance Profiles (response level)", fontsize=13, fontweight="bold")
ax.legend(handles=[Line2D([0], [0], marker="o", color="w", markerfacecolor="#c0504d", markersize=12, label="Eastern Models"),
                   Line2D([0], [0], marker="o", color="w", markerfacecolor="#4c86b0", markersize=12, label="Western Models")], fontsize=11)
ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig(f"{FIG}/figure4_mds_plot_novelty.png", dpi=160); plt.close()

# ---------------- Figure 5: EGR bar chart (six qualifying combos) ----------------
egr = pd.read_csv(ROOT / "results" / "response_grain" / "egr_inclusion.csv")
qual = egr[(egr.ci_sig) & (egr.d_resp > 0) & (egr.cost_savings >= 0)].copy()
qual["label"] = qual.model + "\n" + qual.persona.str.replace("Culture_", "C")
fig, ax = plt.subplots(figsize=(11, 6))
colors = ["#c0504d" if m in EASTERN else "#4c86b0" for m in qual.model]
ax.bar(qual.label, qual.EGR, color=colors, edgecolor="black")
for i, v in enumerate(qual.EGR):
    ax.text(i, v + 0.12, f"{v:.2f}", ha="center", fontsize=12, fontweight="bold")
for thr, name in [(1, "economic"), (2, "strong"), (5, "exceptional")]:
    ax.axhline(thr, color="gray", ls="--", lw=1)
    ax.text(len(qual) - 0.4, thr + 0.06, f"EGR={thr} ({name})", fontsize=9, color="gray")
ax.set_ylabel("Efficiency Gain Ratio", fontsize=12)
ax.set_title("EGR for Novelty: Significant Positive Combinations (response level)", fontsize=14, fontweight="bold")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout(); plt.savefig(f"{FIG}/figure5_egr_bar_chart_novelty.png", dpi=160); plt.close()

# ---------------- Figure 6: cost-performance frontier ----------------
fig, ax = plt.subplots(figsize=(10, 6.5))
for _, r in qual.iterrows():
    col = "#c0504d" if r.model in EASTERN else "#4c86b0"
    ax.scatter([r.cost_savings * 100], [r.d_resp], s=400 * max(r.cost_savings, 0.05) + 120,
               color=col, edgecolor="black", alpha=0.75, zorder=3)
    ax.annotate(f"{r.model}+{r.persona.replace('Culture_','C')}", (r.cost_savings * 100, r.d_resp),
                textcoords="offset points", xytext=(10, 6), fontsize=10)
ax.axhline(0, color="gray", ls="--", lw=1)
# Pareto frontier (maximize savings AND d): best-d point at each savings level that
# is not dominated; the max-savings point is always included (nothing dominates it).
_pts = qual.assign(sav=qual.cost_savings * 100)
frontier, best_d = [], -np.inf
for sav in sorted(_pts.sav.unique()):
    dmax = _pts.loc[_pts.sav == sav, "d_resp"].max()
    if dmax > best_d or sav >= _pts.sav.max() - 1e-9:
        frontier.append((sav, dmax)); best_d = max(best_d, dmax)
ax.plot([f[0] for f in frontier], [f[1] for f in frontier], color="black", lw=1.5,
        zorder=2, label="Pareto frontier")
ax.legend(fontsize=10)
ax.set_xlabel("Cost savings vs own large model (%)", fontsize=12)
ax.set_ylabel("Cohen's d (Novelty, response level)", fontsize=12)
ax.set_title("Cost-Performance: Significant Positive Combinations", fontsize=14, fontweight="bold")
ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig(f"{FIG}/figure6_cost_performance_frontier_novelty.png", dpi=160); plt.close()

# ---------------- Appendix: mean vs median ----------------
cells = resp[resp.condition.isin(CONDS4)].groupby(["family", "condition"])["Novelty"].agg(["mean", "median"])
r, pv = stats.pearsonr(cells["mean"], cells["median"])
fig, ax = plt.subplots(figsize=(7.5, 7))
ax.scatter(cells["median"], cells["mean"], s=90, color="#4c86b0", edgecolor="black", alpha=0.8)
lo, hi = 1.0, 4.1
ax.plot([lo, hi], [lo, hi], color="gray", ls="--", lw=1)
ax.set_xlabel("Median Novelty (response level)", fontsize=12)
ax.set_ylabel("Mean Novelty (response level)", fontsize=12)
ax.set_title(f"Mean vs Median Novelty (r = {r:.3f})", fontsize=14, fontweight="bold")
ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig(f"{FIG}/appendix_mean_vs_median_novelty.png", dpi=160); plt.close()

print("qualifying combos for EGR/frontier:")
print(qual[["model", "persona", "d_resp", "cost_savings", "EGR"]].to_string(index=False))
print("MDS coords:", dict(zip(prof.index, xy.round(2).tolist())))
print("figures written to", FIG)

# ---------------- Figure 7: inter-rater reliability (full data, both grains) ----------------
kap = pd.read_csv(ROOT / "results" / "response_grain" / "fleiss_kappa.csv")
dims = kap["dimension"].tolist()
k9 = kap["kappa_9raters_all"].tolist()
k3 = kap["kappa_3judgerounds_all"].tolist()
fig, ax = plt.subplots(figsize=(11, 6))
x = np.arange(len(dims)); w = 0.38
b1 = ax.bar(x - w/2, k9, w, color="#4c86b0", edgecolor="black", label="9 ratings per response")
b2 = ax.bar(x + w/2, k3, w, color="#7dab87", edgecolor="black", label="3 judge-level means")
for bars in (b1, b2):
    for b in bars:
        ax.annotate(f"{b.get_height() + 1e-9:.2f}", (b.get_x() + b.get_width()/2, b.get_height()),
                    textcoords="offset points", xytext=(0, 4), ha="center", fontsize=11, fontweight="bold")
for yv, lab, col in [(0.20, "Fair (0.20)", "#c0504d"), (0.40, "Moderate (0.40)", "#e8a33d"),
                     (0.60, "Good (0.60)", "#2e7d32"), (0.75, "Excellent (0.75)", "#1b5e20")]:
    ax.axhline(yv, color=col, ls="--", lw=1.2, label=lab)
ax.set_xticks(x); ax.set_xticklabels(dims, fontsize=11)
ax.set_ylabel("Fleiss' Kappa (κ)", fontsize=12)
ax.set_xlabel("Creativity Dimension", fontsize=12)
ax.set_title("Inter-Rater Reliability by Dimension (full data, 3,516 responses)", fontsize=14, fontweight="bold")
ax.set_ylim(0, 0.85)
ax.legend(fontsize=9, ncol=2)
ax.grid(alpha=0.3, axis="y")
plt.tight_layout(); plt.savefig(f"{FIG}/figure7_inter_rater_reliability.png", dpi=160); plt.close()
print("figure7 written")
