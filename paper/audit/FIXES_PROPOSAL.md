# Fix proposal — "Doing More with Less: How Cultural Personas Bridge the Cost-Performance Gap in LLMs"

Date: 2026-09-25. Draft analyzed: `Youssef_Hariri_doing_more_with_less_llm_personas.pdf` (36 pp., dated April 12 2026).
Method: claim-to-evidence audit (numeric layer) + semantic claim sweep (meaning layer), built on and cross-checked
against `CORRECTIONS_MEMO.md` and its pipeline (`recompute_all.py` → `recompute/`, log `recompute/run_log.txt`).

---

## Part 0 — Verification of the other agent's memo (what I re-checked myself)

I did not take the memo on trust. Independent checks performed:

| Check | Result |
|---|---|
| Re-ran `recompute_all.py` in `paper_4/venv` (statsmodels 0.14.6 / scipy 1.11.4) | **Reproduces `recompute/run_log.txt` byte-for-byte** (seeded bootstrap, deterministic) |
| `/tmp/repo_unified.csv` (pipeline input) vs GitHub `youssef-hariri/persona-model-fit` `data/unified_evaluations.csv` | **Identical** (git blob sha `29e197da…` matches the live repo) |
| Local `unified_evaluations_fixed_gemini.csv` defects | **Confirmed**: `judge` is 100 % NaN for all 4,645 openai + 4,481 gemini rows (= 9,126, memo's exact count); `variation`/`prompt_variation` are NaN for *all* rows; gemini `custom_id`s are mangled (raw problem text and thought-traces embedded, models mislabeled, e.g. an openai row carrying `..._claude_sonnet_Culture_5_...`). The repo export is the only usable source — memo §0 stands |
| Memo §3 regional means of the 21 d's | **Verified exactly** (rating: C5 East +0.198 / West +0.370, CE +0.053/+0.120, C11 −0.258/−0.150; response: +0.218/+0.449, +0.050/+0.140, −0.316/−0.213) |
| Memo §7 Gemini/Llama/Mistral overall means; Claude 3.10 (1.05) | **Verified** (Gemini 1.391; next lowest Llama = Mistral = 2.275; Claude overall 3.097/1.046) |

### Corrections and refinements to the memo itself

1. **Table 4 is not "unreproducible from nowhere" — it is a *stale artifact*.** The published ANOVA
   (F = 192.89 / 894.77 / 2.58, p = 0.052, residual df 25,297, SS 429.53/664.17/5.74) matches
   `results as of April 8/anova_results.csv` **exactly**. That snapshot was computed on a superseded
   dataset (~25,301 rows) whose own effect sizes are wildly different from the released data
   (e.g. Llama Culture_11 d = −0.845 there vs −0.321 now). So the draft mixes current-data tables
   (3, 5, 6, 17) with a pre-fix snapshot table (4). The memo's fix (replace with the response-grain
   table) is unchanged, but the diagnosis is "stale value", and the April-8 snapshot should be
   quarantined so nothing else is silently drawn from it.
2. **Table 1's κ = 0.68 *does* trace to a frozen artifact**: `results_v2/inter_rater_reliability.csv`
   (35 responses, 3 judges: 0.679 / 0.152 / 0.296 / 0.298 / −0.228 — the draft's 0.68/0.15/0.30/0.30/−0.23).
   The defect is therefore not a missing source but (a) an undocumented, unstable 35-response subset
   (memo: across 200 random 35-subsets κ(Novelty) ranges 0.16–0.71) and (b) a full-data value of 0.326
   that contradicts "good agreement". The memo's fix stands; the audit trail should say "subset estimate,
   upper-tail draw", not "not reproducible".
3. **Table 13 (power) — only the aggregates reproduce.** The memo says §4.5.1's power numbers
   "reproduce exactly at the rating grain". True for the summary stats (mean 0.771, 71.4 % ≥ 0.8 —
   both frozen power files agree: `results/power_analysis.csv`, `results_novelty_advanced/power_analysis.csv`).
   But the **per-cell values in Table 13 match no frozen artifact and no grain** (e.g. Claude C5: paper 0.95,
   frozen/recompute 1.00; Gemini C5: paper 0.79, recompute 0.48 — hand-verified). Table 13's cells are
   paper-only numbers; replace the whole table from `recompute/power_response.csv`.
4. **Memo §6 says "the five published stars" — the draft's Table 17 shows seven** (Llama C5/CE/C11,
   Qwen C5/CE, Mistral C5/C11). Substance unchanged (they match no grain; Claude C5 lacks a star it
   deserves; Qwen CE carries one it doesn't), but the count is 7.
5. **Memo §0's "20 rows differ in score" between repo and local files — not independently reproduced.**
   My merges on parsed (judge, var, problem, model, condition) keys (13,477 rows) and on normalized
   `custom_id` found 0 score differences; the memo author's exact key normalization wasn't available.
   The structural defects of the local file (point 3 of table above) are confirmed and are sufficient
   grounds to use the repo export; treat the "20 rows" figure as *unverified* until the merge is
   re-documented. Low materiality either way.

**Bottom line on the memo: every load-bearing number in it that I re-derived checked out, the pipeline
re-runs deterministically, and its correction tables can be used as-is.**

---

## Part 1 — New defects found by my sweep (not in the memo)

Class legend: **SV** stale value · **DF** direction flip · **AE** attribution/labeling error ·
**PO** paper-only number · **IC** internal inconsistency · **BO** boundary overreach · **ED** editorial.

| # | Location | Draft says | Data says | Class |
|---|---|---|---|---|
| N1 | **Abstract** | "Culture 11 consistently harmed Novelty across all domains (d = −0.170 to −0.198)" | Own Table 6: the four domain d's are −0.170, **−0.118**, −0.198, −0.124 → range is **−0.118 to −0.198** | IC/SV |
| N2 | **§4.1.1** | "Gemini … approximately **1.8 points below the next lowest model**" | Gemini overall 1.391; next lowest (Llama = Mistral) 2.275 → gap **0.88**. 1.78 is the gap to the *highest* model (Claude 3.168) | AE |
| N3 | **§4.7** | "anomalously low **baseline** Novelty scores (M = 1.39 vs. 2.69 average for other models)" | 1.39 and 2.69 are the *all-condition* means; the baseline (Large_Baseline) values are **1.41 vs. 2.60** | AE |
| N4 | **§5.2.2** | "unusually low baseline Novelty scores (1.41 vs. **2.64** average for other models)" | Other models' baseline mean = **2.60** (2.64 is the median; §4.7 quotes 2.69 for the same comparison — three sections, three values) | IC |
| N5 | **Table 13 (§A.4)** | per-cell powers 0.95/0.82/0.78, 0.92/0.98/0.76, … | Match **no** frozen artifact and no grain (see Part 0.3). Cells are paper-only | PO |
| N6 | **§3.2.1 and §5.3** | "see Section 4.6" / "as detailed in Section 4.6" (Gemini anomaly) | The anomaly section is **§4.7** (§4.6 is the summary table) | ED |
| N7 | **Table 2 note vs Table 11** | "n = 900 per condition except: GPT Culture 5 = 1,063; DeepSeek Large Baseline = 884" | Table 11 shows ~15 other cells ≠ 900 (Claude 893/890/893/893; DeepSeek 893/893/896; GPT 890/882/889; Mistral LB 891; Qwen C11 899; Gemini 893/888/888/884) | IC |
| N8 | **§3.7.1 vs Table 3** | §3.7.1: "small (|d| < 0.5), medium (0.5–0.8), large (≥ 0.8)" — no "negligible" | Table 3 caption uses negligible < 0.2 / small 0.2–0.5 / medium / large. Under §3.7.1, e.g. Qwen C5 (−0.185) is "small"; Table 3 calls it "Negligible" | IC |
| N9 | **§5.1.1** | "smaller models (**DeepSeek, 7B parameters**) outperform larger models (Mistral, 24B) in persona effectiveness" | deepseek-chat is DeepSeek-V3, a **671B-total / 37B-active MoE** — not 7B. The "raw parameter count is not a reliable predictor" argument is built on a wrong parameter count (and Mistral's 24B is the *large* of its pair while "small" Mixtral-8x7B is ~47B) | AE/BO |
| N10 | **§3.7.4 vs results** | "ANOVA Assumptions: Shapiro-Wilk …; Levene's test …" promised | The tests exist (`advanced_stats_novelty.txt`: Shapiro-Wilk p = 0.0000 "normality violated"; Levene p = 0.0000 "homogeneity violated") and are **never reported**. Disclose and motivate the response-grain OLS/robust-SE choice accordingly | SV/suppressed |
| N11 | **§4.2.2 / §5.1.2** | "statistically significant moderation effect (t = 2.08, p = 0.037)" | Matches **no** frozen artifact. Closest live value: Culture_Expert × East interaction, rating grain t = 2.118, p = 0.034; response grain t = 0.87, p = 0.38 (memo §3) | SV/PO |
| N12 | **§2.4.2 + references vs contribution 4** | EGR presented as existing literature, cited "(Name, 2026)"; reference list has placeholder "Name, Y. (2026, March)" | Contribution 4 says "we **introduce** the Efficiency Gain Ratio". Either it is novel (then remove the fake prior citation and the placeholder reference) or prior (then fix the citation and drop "introduce"). Also the EGR value-tier thresholds (>1/>2/>5/>10) currently rest on that placeholder — give them a real source or label them as this paper's heuristic | AE/ED |
| N13 | **§4.2.1 / Table 4** | "model family (2 levels: Eastern vs. Western)"; Table 4 row "Model Family" | The factor is **training region**, not model family; elsewhere "model family" means Claude/GPT/…. Rename to Region everywhere in this analysis | AE |
| N14 | **Table 16 (§A.7)** | rows labeled "Baseline" | Ambiguous: Small or Large Baseline? Label explicitly | ED |
| N15 | **§4.5.2, §4.5.4, Table 14, §A.1** | LOO (0.039 mean \|∆\|; Table 14), train-test (0.305/0.274, 0.099/0.119, −0.149/−0.138), mean–median r = 0.997 | Artifacts **exist** (`results_novelty_advanced/leave_one_out_summary.csv` matches Table 14 exactly; `advanced_stats_novelty.txt` matches train-test) — but they are rating-grain-era outputs. Re-run at the response grain (extend `recompute_all.py`) before republication; the stability *pattern* is unlikely to change but the numbers must be the corrected-grain ones | SV (mild) |

Also confirmed from the frozen artifacts: a **mediation analysis exists** (`results/mediation_results.csv`,
identical in the April-8 snapshot) with counter-intuitive suppression patterns (Culture_5: indirect +0.196,
direct −0.250) that the paper never mentions. Either report it or delete it from the repo — a reviewer who
finds it will ask.

---

## Part 2 — Consolidated fix plan (memo fixes, verified, + new fixes)

Priority: **P0** = inference-changing (must fix before resubmission) · **P1** = wrong numbers ·
**P2** = framing/consistency · **P3** = editorial/hygiene.

### P0-1. Unit of analysis everywhere (memo §1 — verified)

The paper's tables treat each of the 9 judge ratings of a response as independent (n ≈ 900/condition);
the independent unit is the **response** (N = 3,516; ≈ 100/model×condition). Every p-value, CI and power
figure is ~9× inflated.

- **Abstract**, replace "we analyze over 25,000 responses" with:
  > "Using 100 problems spanning four domains … we analyze 31,605 judge ratings of 3,516 model responses using a multi-judge evaluation framework."
- **§3.6 (new paragraph):**
  > "All inferential statistics treat the response (mean of the nine judge ratings) as the unit of analysis; judge and prompt-variation are within-response replications, not independent observations."
- **Tables 2 & 11**: keep means (unchanged to ±0.02); replace SDs and n with the response-grain values
  (memo §1 table — reproduced in `recompute/run_log.txt` R3). Fix the Table 2 note (N7): state
  "n = 100 responses per cell, except GPT Culture_5 = 120 and Gemini/Mistral Large_Baseline = 99;
  rating counts vary slightly by cell due to parse-failure exclusions (see Table 11)".
- **Table 3**: replace with the response-grain table (memo §1, `recompute/effect_sizes_response.csv`).
  Headline changes: 11/21 significant (was 15/21); Claude C5 d = 1.087 [0.800, 1.417]; Llama C5, Mistral C5,
  GPT C11, Qwen C5 **lose** significance; **Gemini C11 gains** significance (d = −0.443 [−0.701, −0.182]).
  Cascade: abstract, §4.1.2–4.1.3, Table 9 row 1, §5.1.1, §5.2.1–5.2.2, Table 10, §6 — every place that
  quotes d or counts significant comparisons.

### P0-2. ANOVA (memo §2 + my Part 0.1)

Table 4 is a stale April-8-snapshot artifact. Replace with the response-grain table
(`recompute/anova_response.csv`): persona F(3, 2810) = 35.75, p < 0.001; region F(1, 2810) = 61.51,
p < 0.001; interaction **F(3, 2810) = 0.89, p = 0.445**. Replace "marginally significant interaction
(F(3, 25297) = 2.58, p = 0.052)" with "no persona × region interaction at the response level
(F(3, 2810) = 0.89, p = 0.445)". Rename the factor "Model Family" → "Region" (N13). Report the
assumption violations (N10) and justify the approach (large-sample OLS + response-grain averaging;
optionally HC3 robust SEs, which the recompute already shows for the moderation specs).

### P0-3. Regional moderation (memo §3 — numbers verified; N11)

- Delete "Eastern models show greater responsiveness to cultural personas, particularly Culture_Expert"
  (§4.2.2 end, §4.2.4, §5.1.2, Table 9 row 2). At the response grain nothing survives: binary interaction
  t = −1.27, p = 0.21; Culture_Expert × East t = 0.87, p = 0.38 (HC3: −0.09/0.93, 0.94/0.35).
- The §4.2.2 per-persona "d" paragraph (CE: +0.144 vs +0.023 "sixfold"; C5: −0.049 vs −0.064;
  C11: −0.338 vs −0.345) matches no grain — and the actual region means point the *other* way for the
  positive personas (Western larger at both grains; verified). Replace with:
  > "Training region did not moderate persona effects at the response level (interaction t = −1.27,
  > p = 0.21; Bayes Factor = 0.331, anecdotal evidence against moderation). Apparent frequentist
  > significance at the rating grain is an artifact of treating nine judge ratings per response as
  > independent."
- Keep the BF = 0.331 (it already pointed the right way) — the corrected analysis now *agrees* with it,
  which is a cleaner story: "the Bayesian evidence was right; the frequentist significance was an
  artifact." Fix §5.1.2 accordingly (drop the t = 2.08/p = 0.037 — N11 — or footnote it as the
  rating-grain artifact).

### P0-4. Inter-rater reliability (memo §4 + my Part 0.2)

- Table 1, §3.6.3, §4 opening, §5.1.4, abstract: replace κ = 0.68 with the full-data values, rater
  structure stated: 9 raters/response: **0.33 / 0.32 / 0.32 / 0.31 / 0.17** (Novelty/Usefulness/
  Flexibility/Elaboration/Cultural Sensitivity); 3 judge-round means: 0.40/0.26/0.31/0.30/0.07.
- Novelty becomes "fair-to-moderate", not "the only dimension with good agreement" — and note the four
  core dimensions are statistically indistinguishable (0.31–0.33), so the Novelty focus must be
  re-justified on **theoretical** grounds ( Novelty is the construct the research question is about;
  the other dimensions are reported as exploratory) plus a limitations sentence, not on reliability
  superiority. Alternatively/additionally: human-rater validation subset (§5.4 already gestures at this).
- Explain the 35-response subset (§3.6.3): state that the earlier subset estimate (κ = 0.68) was
  retained only as a historical artifact, or remove it; per the memo, across random 35-response subsets
  κ(Novelty) ranges 0.16–0.71, so any single-subset number is uninformative.

### P0-5. Post-hoc power (memo §5 + my N5)

- Replace **all of Table 13** from `recompute/power_response.csv` (its current cells match no artifact;
  e.g. Gemini C5 should be ~0.08 at response grain, not 0.79).
- §4.5.1: mean power 0.544, 38.1 % of comparisons ≥ 0.80. Add the honest sentence: most comparisons
  are underpowered at the correct unit of analysis, which is why the corrected CIs (Table 3) widen and
  why non-significant results should be read as "insufficient evidence", not "no effect".

### P0-6. Table 17 stars + closing sentence (memo §6; star count corrected to 7)

- Republish Table 17 with response-grain d, p, p_FDR and stars (9/21: Claude C5; DeepSeek C5; GPT C5;
  Llama C5, C11; Mistral C5, C11; Qwen C5; Gemini C11) from `recompute/pure_persona_fdr_response.csv`.
- Delete or invert the closing "weaker baseline" sentence — false for DeepSeek (0.379 < 0.581) and
  GPT (0.395 < 0.501).
- Label Table 17's baseline means as Small_Baseline (they appear nowhere else).

### P1-1. Descriptive claims (memo §7 + my N1–N4)

- §4.1.1: "DeepSeek showed the largest improvement … +0.71 (+26.9 %)" → the largest is
  **Claude + Culture_5: +0.97 points (+34.2 %)**; DeepSeek is second (+0.71, +27.1 %, response grain).
- §4.1.1: "Claude achieved the highest Novelty scores across all conditions (M = 3.14, SD = 1.22)" →
  "Claude achieved the highest mean Novelty in three of four conditions (M = 3.10, SD = 1.05 across
  conditions); Qwen's unsteered large model matched it (2.83 vs 2.84)."
- §4.1.1: Gemini "1.8 points below the next lowest model" → **0.9 points below the next-lowest models
  (Llama, M = 2.26; Mistral, M = 2.27; Gemini 1.39)**; 1.8 is the gap to the best model (N2).
- §4.7: "baseline Novelty scores (M = 1.39 vs 2.69)" → these are all-condition means; use either
  "overall scores (1.39 vs 2.67)" or "baseline scores (1.41 vs 2.60)" (N3).
- §5.2.2: "1.41 vs. 2.64 average" → 2.60 (mean) — and align §4.7/§5.2.2 on one figure (N4).
- Abstract: "d = −0.170 to −0.198" → **d = −0.118 to −0.198** (or, after the grain correction, use the
  response-grain domain d's: −0.149 to −0.229; `recompute/domain_effects.csv`) (N1).

### P1-2. Economic numbers (memo §8 — verified)

- "36× lower cost ($2.00 vs $25.00)" → **12.5×** (§4.4.2). The 60× DeepSeek figure (59.5×) is fine.
- Abstract/contribution 4: "40–88%" → **40–87%** (88 % is Gemini's rounded 87.5 %; Gemini is excluded
  as non-comparable everywhere else).
- EGR at response-grain means: GPT **9.15** / 8.53 / 8.18; Claude 2.24 / 1.84 / 1.70; DeepSeek
  1.27 / 1.19 / 1.00 (Table 8 and "EGR up to 9.17" → 9.15, twice in abstract + Table 9 + §5.2.3).
- **EGR scale-dependence (now demonstrated):** harmful combinations score "exceptional" EGR —
  Gemini C11 (d = −0.443, sig.) EGR 6.85; Qwen C11 (d = −0.638, sig.) EGR 3.99; Llama C11 (−0.412, sig.)
  3.78 (`recompute/egr_inclusion.csv`). Restrict EGR reporting to CI-significant positive-gain
  combinations, or redefine it on a performance *difference*; add the equal-output-token-count assumption
  (Gemini's reasoning traces violate it) to §3.7.3.
- Tables 7–8: state **one** inclusion rule. Under a CI-significance + cost-savings rule the qualifying
  set is exactly six: Claude C5, Claude CE, DeepSeek C5, DeepSeek CE, GPT C5, GPT CE. Fix "Eight
  model-persona combinations" vs the nine rows, and the DeepSeek 0 %-savings rows under a "lower cost"
  heading.
- Table 10: replace "−0.519 to −0.118" and the "any model" wording: the response-grain significant harms
  are Qwen C11 (−0.638), Mistral C11 (−0.496), Gemini C11 (−0.443), Llama C11 (−0.412), Qwen CE (−0.365).
  Culture_11 is *not* significantly harmful for Claude, DeepSeek or GPT — soften "Avoid Culture 11 across
  all models" (§5.2.1) to "avoid Culture_11 for Qwen, Mistral, Llama and Gemini; it shows no significant
  benefit for any model".

### P2-1. Magnitude scheme (memo §7 + N8)

Unify on: negligible < 0.2, small 0.2–0.5, medium 0.5–0.8, large ≥ 0.8. Apply in §3.7.1 (which currently
omits "negligible"), §4.1.2, Table 3 caption, §4.1.2 Gemini text ("negligible (all |d| < 0.3)" vs
C11 = −0.286 "small" in the same breath — and at the response grain C11 is **medium**, −0.443, so the
"Gemini inert" narrative needs the §4.7 caveat explicitly attached wherever it appears:
§4.1.2, §4.1.3, §5.2.2).

### P2-2. Gemini consistency (memo §9)

State once, in §4.7, which analyses include Gemini and which exclude it, and apply it: Gemini currently
feeds the ANOVA, the moderation test and the MDS narrative despite being declared a measurement artifact.
Domain-pooled effects without Gemini (`recompute/domain_effects.csv`, `d_response_noGemini`:
C5 = 0.287/0.732/0.240/0.647) leave §4.3's GK-and-Reasoning ordering intact — say so explicitly.
Rewrite Figure 3's interpretation as performance-profile similarity, not "Eastern models form a separate
cluster" (DeepSeek sits inside the Claude/GPT region).

### P2-3. FDR scope (memo §10)

§3.7.2 says "BH correction applied to all multiple comparisons", but Table 3's significance is
bootstrap-CI exclusion and only Table 17 uses FDR. State exactly where FDR is and is not used
(and consider applying BH to the 21 Table 3 comparisons for coherence with your own methods section).

### P3. Editorial & housekeeping (memo §10 + N6, N9, N12, N14, N15)

- §3.1 "conducted in March 2025" → **March 2026** (model IDs: gpt-5.4-2026-03-05, claude-opus-4-6,
  gemini-3.1-pro-preview).
- §3.6.1 "temperature = 0.2 to ensure … deterministic scoring" → "to reduce scoring variance"
  (0.2 is not deterministic).
- §3.6.2 vs §3.6.3: all responses were judged by all three judges × 3 variations; explain or remove the
  35-response subset (see P0-4).
- Cross-references: §3.2.1 and §5.3 "Section 4.6" → **Section 4.7** (N6).
- §5.1.1: remove "DeepSeek, 7B parameters" — deepseek-chat is DeepSeek-V3 (671B total / 37B active MoE);
  reframe the argument around cost and architecture class, not parameter count (N9).
- References: fix or delete the placeholder "Name, Y. (2026)"; resolve the EGR novelty-vs-prior-work
  contradiction (N12); give the EGR thresholds (1/2/5/10) a source or label them as this paper's heuristic.
- Table 16: label "Baseline" rows as Small or Large (N14).
- GPT Culture_5 n = 1,063 ratings = 120 responses: explain the 20 extra problems or trim to the
  100-problem set (it changes that cell's weight in every pooled statistic).
- Table 2/Figure 1 omit Small_Baseline although §4.1.1 promises all five conditions — add it or fix the
  promise. Figure 1 caption's red/blue region coloring belongs to Figures 2–3.
- §4.5.3: Isolation Forest with contamination = 0.1 flags ~10 % by construction — "identified 5.1 %"
  is impossible; re-run or restate.
- Repo hygiene: remove `.DS_Store` from the repo; add the `judge` column for openai/gemini rows to the
  public CSV (currently only recoverable from `custom_id`); re-export or delete the broken local
  `unified_evaluations_fixed_gemini.csv`; quarantine `results as of April 8/` (the source of the stale
  Table 4) and either publish or delete the unreported `results/mediation_results.csv`.
- Re-run LOO / train-test / mean-median robustness checks at the response grain (N15).

---

## Part 3 — What survives (verified)

The descriptive core is solid: response-grain means reproduce Tables 2/11 to ±0.02; the contingency
pattern (Claude/DeepSeek benefit; Qwen/Mistral harmed by Culture_11; Gemini inert-to-negative) holds with
corrected CIs; the domain ordering (Culture_5 strongest on General Knowledge and Reasoning; Culture_11
negative in all four domains) holds with and without Gemini; the EGR arithmetic is internally consistent;
LOO/train-test/mean-median artifacts exist and match the draft (pending response-grain re-run). The
**narrative arc survives** — contingency model, domain specificity, economic viability of small+persona —
with a smaller significant set (11/21), no regional moderation, fair-to-moderate judge agreement, honest
power (0.544 mean), and a rule-consistent economic table (six qualifying combinations — 40–87% savings
for GPT and Claude, cost parity for DeepSeek — EGR up to 9.15).

## Appendix — evidence chain for the key replacements

| Claim | Frozen source | Script |
|---|---|---|
| Response-grain d's, CIs, significance (Table 3) | `recompute/effect_sizes_response.csv` (log R4b) | `recompute_all.py` (seed 42, 5,000 bootstrap) |
| Rating-grain reproduction of published Table 3 | `recompute/effect_sizes_rating.csv` (log R4) | same |
| ANOVA both grains (Table 4 replacement) | `recompute/anova_response.csv`, `anova_rating.csv` (R5) | same |
| Published Table 4 = stale artifact | `results as of April 8/anova_results.csv` (exact match) | — |
| Moderation specs, both grains, HC3 | `recompute/moderation_*.csv` (R6) | same |
| Full-data Fleiss κ (Table 1 replacement) | `recompute/fleiss_kappa.csv` (R7) | same |
| Published κ = 0.68 source | `results_v2/inter_rater_reliability.csv` (35-response subset) | `corrected_inter_rater.py` |
| Power both grains (Table 13 replacement) | `recompute/power_response.csv`, `power_rating.csv` (R8) | same |
| Table 17 replacement | `recompute/pure_persona_fdr_response.csv` (R9) | same |
| Domain effects incl. no-Gemini | `recompute/domain_effects.csv` (R10) | same |
| EGR + inclusion rule | `recompute/egr_inclusion.csv` (R11) | same |
| §4.1.1 claim checks (largest gain, Claude means) | `recompute/run_log.txt` R12 | same |
| LOO / train-test / assumption tests (rating-grain era) | `results_novelty_advanced/leave_one_out_summary.csv`; `advanced_stats_novelty.txt` | `leave_one.py`, `advanced_stats_novelty.py` |
| Repo data = pipeline input | git blob sha `29e197da…` = `/tmp/repo_unified.csv` | — |

## Round-2 addendum (post-application re-audit, September 25, 2026)

After the 99 planned replacements were applied, the corrected draft was re-audited end-to-end against
the frozen artifacts. Eight further refinements were applied (9 additional replacements; 108 total).
Where they refine instructions above, **the values below are final** (full detail in `CHANGE_LOG.md`):

1. **Train–test split (§4.5.3):** final frozen values (`recompute/train_test_response.csv`, seed 42,
   random 80/20 by problem — *not* stratified): Culture_5 train 0.310 / test 0.515 (Δ +0.205);
   Culture_Expert 0.085 / 0.271 (+0.186); Culture_11 −0.186 / −0.097 (+0.089); max |Δ| = 0.21.
   Signs consistent for all three personas. (Values printed by an earlier, pre-final script run
   differed; the CSV cited here is authoritative and re-runs bit-identical.)
2. **Pooled means (§4.1.1):** Llama M = 2.26, Mistral M = 2.27 (an earlier draft of the fix said
   "both 2.28"); verified against `recompute/response_level.csv`.
3. **Non-Gemini pooled mean (§4.7):** 2.67 (not 2.70) — mean of the six other models' pooled means.
4. **Cost framing:** every occurrence of "40–87% lower cost" for the six significant combinations
   now reads "equal or lower cost (40–87% savings for GPT and Claude; cost parity for DeepSeek)",
   because DeepSeek's small/large prices are identical (0% savings).
5. **GPT benefits (§5.2.2):** the non-significant Culture_11 effect (d = 0.231, CI includes zero) is
   no longer listed among GPT's benefits; range is d = 0.344–0.570 (Culture_Expert, Culture_5).
6. **Figures:** MDS plot regenerated with non-overlapping Llama/Mistral labels; cost-performance
   figure regenerated with the Pareto-frontier line its caption promises
   (DeepSeek+C5 → Claude+C5 → GPT+C5).

No other instruction in this document was altered by the re-audit.
