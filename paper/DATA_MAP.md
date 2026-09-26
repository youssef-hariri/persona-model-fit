# Data Map — claim-to-evidence mapping for the revised draft

**Paper:** "Doing More with Less: How Cultural Personas Bridge the Cost-Performance Gap in LLMs"
**Draft under audit:** `paper4_v2_corrected.tex` (revised September 25, 2026)
**Unit of analysis:** the response (mean of nine judge ratings); N = 3,516 responses, 31,605 ratings.

Every quantitative claim in the revised draft traces to a frozen artifact below. Pipelines:
`recompute_all.py` (log: `recompute/run_log.txt`; seed 42, 5,000-resample bootstrap) and
`recompute_robustness.py` (sections B1–B6). Both re-run bit-identical (md5-verified).
Source data identical to the released repository (git blob sha `29e197da…`).

| # | Claim (location in draft) | Final value | Frozen source | Script |
|---|---|---|---|---|
| D1 | Sample size (abstract, §3.5, §3.7.2) | 31,605 ratings of 3,516 responses; ~100/cell; 2,818 in persona × region analyses | `recompute/run_log.txt` R2; `recompute/response_level.csv` (3,516 rows) | `recompute_all.py` |
| D2 | Descriptive means/SD/n (Tables 2, 11) | e.g. Claude C5 3.81 (0.64), n=100; GPT C5 n=120; Gemini/Mistral LB n=99 | `recompute/descriptives_response.csv` (R2/R3) | same |
| D3 | Effect sizes + bootstrap CIs (Table 3, forest plot) | 21 d's; 11/21 significant; Claude C5 1.087 [0.800, 1.417]; Qwen C11 −0.638 | `recompute/effect_sizes_response.csv` (R4b) | same |
| D4 | Two-way ANOVA (Table 4) | Persona F(3,2810)=35.75; Region F(1,2810)=61.51; interaction F=0.89, p=0.445 | `recompute/anova_response.csv` (R5) | same |
| D5 | Old Table 4 provenance note | old p=0.052 = superseded extract; rating-grain live value p=0.0004 | `results as of April 8/anova_results.csv` (exact match); `recompute/anova_rating.csv` | — |
| D6 | Moderation regression (Table 5, §5.1.2) | interaction t=−1.27, p=0.206; BF=0.331; CE×East t=0.87, p=0.383 (HC3 0.349) | `recompute/moderation_response.csv`, `moderation_rating.csv` (R6) | same |
| D7 | Region descriptive effects (§4.2.2) | C5: +0.449 W vs +0.218 E; CE: +0.140 vs +0.050; C11: −0.213 vs −0.316 | computed from `recompute/effect_sizes_response.csv` | same |
| D8 | Inter-rater reliability (Table 1, §3.6) | κ (9 ratings): 0.33/0.32/0.32/0.31/0.17; (3 judge means): 0.40/0.26/0.31/0.30/0.07 | `recompute/fleiss_kappa.csv` (R7) | same |
| D9 | Old κ=0.68 provenance + instability | 35-response subset (0.679); 200 random subsets → κ(Novelty) 0.16–0.71, median 0.39 | `results_v2/inter_rater_reliability.csv`; `CORRECTIONS_MEMO.md` §4 | `corrected_inter_rater.py` |
| D10 | Domain effects (Tables 6, 12, heatmap) | C5 0.233/0.628/0.185/0.545; CE 0.036/0.223/0.092/0.210; C11 −0.196/−0.154/−0.229/−0.149; no-Gemini C5 0.287/0.732/0.240/0.647 | `recompute/domain_effects.csv` (R10) | same |
| D11 | EGR + inclusion rule (Tables 7, 8, EGR chart) | 6 qualifying combos: GPT 9.15/8.53; Claude 2.24/1.84; DeepSeek 1.27/1.19; savings 87/87/40/40/0/0% | `recompute/egr_inclusion.csv` (R11) | same |
| D12 | Cross-model cost claims (§4.4.2, §5.2.3) | DeepSeek+C5 ≈ Opus at ~60× ($0.42 vs $25.00); GPT+C5 at 12.5× ($2.00 vs $25.00) | price list in Appendix A.6 (unchanged from draft) | — |
| D13 | Post-hoc power (Table 13, §4.5.1) | response-level mean 0.544; 38.1% ≥ 0.80 (range 0.05–1.00) | `recompute/power_response.csv` (R8) | same |
| D14 | Leave-one-out (Table 14, §4.5.2) | mean \|Δ\|=0.047; 19/21 < 0.1; max 0.117 (Claude, C5); Qwen 0.083 … Llama 0.018 | `recompute/loo_response.csv`, `loo_summary_response.csv` | `recompute_robustness.py` (B1) |
| D15 | Train–test split (§4.5.4 Generalizability) | C5 0.310/0.515 (+0.205); CE 0.085/0.271 (+0.186); C11 −0.186/−0.097 (+0.089); random 80/20 by problem, seed 42 | `recompute/train_test_response.csv` | same (B2) |
| D16 | Outlier analysis (§4.5.3 Outlier Analysis) | Isolation Forest flags 10.0% by construction; pooled d shifts ≤ 0.031 | script stdout (B4) | same (B4) |
| D17 | ANOVA assumption checks (§4.2.1) | Shapiro–Wilk p=9.4e-29; Levene p=0.0025 (both violated; disclosed) | script stdout (B5) | same (B5) |
| D18 | GPT duplicate problems (Table 2 note, limitations) | 120 responses / 100 problems; per-problem averaging: d=0.624 vs 0.570 | script stdout (B6) | same (B6) |
| D19 | Mean vs median (A.1) | r=0.983 (p=1.6e-20), 28 cells; diffs −0.33 to +0.36 | `recompute/mean_median_response.csv` | same (B3) |
| D20 | Other dimensions (Table 16, A.7) | 7 models × 4 conditions × 4 dimensions (response-level means) | `recompute/other_dims_response.csv` | same |
| D21 | Pure persona effects (Table 17, A.8) | 9/21 significant (BH-FDR); Claude C5 1.101*; small baselines > large baselines for DeepSeek (2.91 vs 2.64) and GPT (2.76 vs 2.64) | `recompute/pure_persona_fdr_response.csv` (R9) | `recompute_all.py` |
| D22 | Pooled means (§4.1.1, §4.7, §5.2.2) | Claude 3.10 (SD 1.05); Gemini 1.39; Llama 2.26; Mistral 2.27; non-Gemini pooled 2.67; large-baseline contrast 1.41 vs 2.60 | computed from `recompute/response_level.csv` | — |
| D23 | §4.1.1 comparative claims | Claude C5 +0.97 (+34.2%); DeepSeek +0.71 (+27.1%, second); Qwen C11 −0.58 (−20.3%) | `recompute/run_log.txt` R12; recomputed from D2 | `recompute_all.py` |
| D24 | Figures 1–8 | response-grain renders of D2, D3, D8, D10, D11, D19; MDS of D2 profiles; Figure 1 = inter-rater reliability (added in revision; the asset existed but was never included in the submitted draft) | `figures_v2/*.png` | `generate_figures_v2.py` |
| D25 | Old-rating-grain reproductions (audit trail) | published Tables 2/3/13 aggregates reproduce at rating grain | `recompute/*_rating.csv`; `results/power_analysis.csv`; `results_novelty_advanced/leave_one_out_summary.csv` | `recompute_all.py`, `leave_one.py` |

**Items with no frozen source (intentional):** price list (A.6) is manually sourced from provider
pricing pages; EGR value-tier thresholds (>1/>2/>5/>10) are this paper's heuristic (stated in §3.7.3).
The unreported mediation analysis in `results/mediation_results.csv` is flagged for a report-or-delete
decision (`FIXES_PROPOSAL.md`, Part 1 note) — it is not cited anywhere in the revised draft.
