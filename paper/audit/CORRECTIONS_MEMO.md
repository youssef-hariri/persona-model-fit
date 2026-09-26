# Corrections memo — "Doing More with Less: How Cultural Personas Bridge the Cost-Performance Gap in LLMs"

Generated 2026-09-25 from the raw evaluation data. All recomputations: `recompute_all.py`
(outputs in `recompute/`; full log `recompute/run_log.txt`), run in `paper_4/venv`
(the same statsmodels 0.14.6 / scipy 1.11.4 stack as the original analysis).

## 0. Data provenance and protocol

- **Analysis source:** the public repo export `data/unified_evaluations.csv` (31,605 rating
  rows). The local `unified_evaluations_fixed_gemini.csv` has the same 31,605 rows but its
  `judge`/`judge_model` columns are **empty for all openai and gemini rows** and its
  `custom_id` values are **misaligned with the score columns** for those families
  (e.g. a row with `model_family=openai` carries `..._claude_sonnet_Culture_5_...`), so judge
  identity and response identity cannot be recovered from it for 9,126 rows. Use the repo
  export; re-export the local file or document the defect.
- **Local vs repo sync:** 22,575 rating rows match on (custom_id, judge, variation) with
  non-missing scores; **20 rows differ in score** between the two files, and 1 row is NaN in
  the repo file but has a value locally. The public export is not byte-consistent with the
  working file — reconcile before resubmission.
- **Grains.** One *response* = one model output to one problem. Each response was scored by
  3 judges × 3 prompt variations = **9 rating rows**. The file holds 31,605 ratings =
  **3,516 responses** (2,818 in the three persona conditions + Large_Baseline). 20 responses
  (GPT Culture_5, Gemini) appear merged in the raw grouping with 17–18 ratings; they were
  split into copies via the duplicated (judge, variation) index (`copy` column in
  `recompute/response_level.csv`).
- **The paper's tables are computed at the rating grain** (each of the 9 judge ratings of a
  response treated as an independent observation). This was verified: the rating-grain run
  reproduces Table 3 (all 21 d and CIs), Table 5 (coefficients 2.3042/0.4326/0.1480/−0.1337,
  t = −3.413), Table 6 (all 12 domain d), Table 17's d column (all 21), and §4.5.1's power
  numbers (mean 0.771, 71.4% ≥ 0.8) exactly. Corrected values below are the **response grain**
  (ratings averaged within response), which is the defensible unit of analysis.
- Missing scores (~180 rating rows, e.g. `parsing_notes` = "Novelty:colon") are dropped
  per dimension; this reproduces the paper's per-cell n (893, 884, 1063, …).

## 1. Unit of analysis and sample size (Abstract, §3.5–3.6, §4.1, Tables 2, 3, 11, 13)

**Problem.** n = 900 per condition and "over 25,000 responses" are rating counts; the
independent N is 3,516 responses (≈100 per model×condition). Every p-value, CI and power
figure in the paper is inflated ~9×.

**Corrected numbers (response grain):**

- Table 2/11 means are unchanged to ±0.02; SDs and n must be replaced:

| Model | C5 mean (SD), n | CE mean (SD), n | C11 mean (SD), n | LB mean (SD), n |
|---|---|---|---|---|
| Claude | 3.81 (0.64), 100 | 3.14 (1.06), 100 | 2.89 (0.95), 100 | 2.84 (1.09), 100 |
| DeepSeek | 3.35 (1.02), 100 | 3.14 (1.03), 100 | 2.64 (1.00), 100 | 2.64 (1.13), 100 |
| GPT | 3.22 (0.99), 120 | 3.00 (1.04), 100 | 2.88 (1.02), 100 | 2.64 (1.06), 100 |
| Gemini | 1.49 (0.73), 100 | 1.45 (0.56), 100 | 1.21 (0.34), 100 | 1.41 (0.55), 99 |
| Llama | 2.50 (0.74), 100 | 2.34 (0.68), 100 | 1.97 (0.68), 100 | 2.29 (0.86), 100 |
| Mistral | 2.50 (0.74), 100 | 2.29 (0.74), 100 | 1.95 (0.80), 100 | 2.36 (0.85), 99 |
| Qwen | 2.63 (0.71), 100 | 2.51 (0.69), 100 | 2.26 (0.72), 100 | 2.83 (1.05), 100 |

- Corrected Table 3 (d [95% bootstrap CI], significance = CI excludes 0; 11/21 significant):

| Model | Persona | d | 95% CI | sig |
|---|---|---|---|---|
| Claude | Culture_5 | 1.087 | [0.800, 1.417] | yes |
| Claude | Culture_Expert | 0.281 | [0.012, 0.574] | yes |
| Claude | Culture_11 | 0.056 | [−0.213, 0.337] | no |
| DeepSeek | Culture_5 | 0.664 | [0.384, 0.993] | yes |
| DeepSeek | Culture_Expert | 0.464 | [0.186, 0.770] | yes |
| DeepSeek | Culture_11 | 0.006 | [−0.264, 0.285] | no |
| GPT | Culture_5 | 0.570 | [0.308, 0.868] | yes |
| GPT | Culture_Expert | 0.344 | [0.070, 0.647] | yes |
| GPT | Culture_11 | 0.231 | [−0.043, 0.521] | no |
| Llama | Culture_5 | 0.271 | [−0.006, 0.561] | no |
| Llama | Culture_Expert | 0.076 | [−0.196, 0.363] | no |
| Llama | Culture_11 | −0.412 | [−0.693, −0.131] | yes |
| Mistral | Culture_5 | 0.186 | [−0.094, 0.461] | no |
| Mistral | Culture_Expert | −0.077 | [−0.367, 0.203] | no |
| Mistral | Culture_11 | −0.496 | [−0.816, −0.215] | yes |
| Qwen | Culture_5 | −0.229 | [−0.504, 0.040] | no |
| Qwen | Culture_Expert | −0.365 | [−0.642, −0.097] | yes |
| Qwen | Culture_11 | −0.638 | [−0.925, −0.366] | yes |
| Gemini | Culture_5 | 0.131 | [−0.154, 0.396] | no |
| Gemini | Culture_Expert | 0.076 | [−0.205, 0.355] | no |
| Gemini | Culture_11 | −0.443 | [−0.701, −0.182] | yes |

  vs the paper: Llama C5, Mistral C5, GPT C11, Qwen C5 **lose** significance; Gemini C11
  **gains** it (and is medium-sized, contradicting "negligible effects across all personas",
  §4.1.2/§4.7/§5.2.2). Headline effects get larger but less precise (Claude C5 0.908 → 1.087).

**Replacement text (abstract):** "Using 100 problems spanning four domains … we analyze
31,605 judge ratings of 3,516 model responses using a multi-judge evaluation framework."
Add to §3.6: "All inferential statistics treat the response (mean of the nine judge ratings)
as the unit of analysis; judge and prompt-variation are within-response replications, not
independent observations."

## 2. Two-way ANOVA (Table 4, §4.2.1)

**Problem.** Table 4 is not reproducible at any grain from the released data. Rating grain:
persona F(3, 25194) = 234.96; region F(1, 25194) = 401.96; **interaction F(3, 25194) = 6.06,
p = 0.0004**. Response grain: persona F(3, 2810) = 35.75; region F(1, 2810) = 61.51;
**interaction F(3, 2810) = 0.89, p = 0.445**. The published F = 2.58, p = 0.052 matches
neither, and its residual df (25,297) exceeds the number of rating rows available (25,202).

**Replacement:** report the response-grain table and replace "marginally significant
interaction (F(3, 25297) = 2.58, p = 0.052)" with "no persona × region interaction at the
response level (F(3, 2810) = 0.89, p = 0.445)". The "marginally significant" framing must go:
at the rating grain the same interaction is p = 0.0004, i.e. the published value sits between
two grains and belongs to neither.

## 3. Regional moderation (§4.2.2, Table 5, §4.2.4, §5.1.2, abstract)

**Problem.** Three different models are conflated:
- Table 5 = rating-grain binary spec (persona vs Large_Baseline × East); reproduced exactly,
  interaction **−0.134, t = −3.41** (Eastern *less* responsive to personas overall).
- The text's "t = 2.08, p = 0.037 … Eastern models show greater responsiveness" is the
  **Culture_Expert × East term of a different, persona-level spec** (rating grain:
  +0.100, t = 2.12, p = 0.034). Opposite sign, different hypothesis.
- The paragraph's per-persona "d" values (Culture_5: −0.049 East vs −0.064 West;
  Culture_11: −0.338 vs −0.345; "sixfold difference" 0.144 vs 0.023) match **no** grain.
  Actual region means of the 21 combination d's — rating grain: C5 East +0.198 vs West
  +0.370, CE +0.053 vs +0.120, C11 −0.258 vs −0.150; response grain: C5 +0.218 vs +0.449,
  CE +0.050 vs +0.140, C11 −0.316 vs −0.213. Western means are *larger* for the positive
  personas at both grains.
- At the response grain nothing survives: binary interaction t = −1.27, p = 0.21;
  Culture_Expert × East t = 0.87, p = 0.38 (HC3-robust: −0.09/0.93 and 0.94/0.35).

**Replacement (§4.2.2, §4.2.4, §5.1.2, abstract, Table 9 row 2):** "Training region did not
moderate persona effects at the response level (interaction t = −1.27, p = 0.21; Bayes
Factor = 0.331, anecdotal evidence against moderation). Apparent frequentist significance at
the rating grain (t = −3.41, binary spec; t = +2.12 for Culture_Expert × East, persona spec)
is an artifact of treating nine judge ratings per response as independent." Delete "Eastern
models show greater responsiveness to cultural personas, particularly Culture_Expert".

## 4. Inter-rater reliability (Table 1, §3.6.3, §4 opening, §5.1.4)

**Problem.** κ = 0.68 ("good") is not reproducible. Full-data Fleiss κ (9 raters per
response): Novelty **0.326**, Usefulness 0.321, Flexibility 0.316, Elaboration 0.311,
Cultural Sensitivity 0.171. With 3 judge-level rounded ratings: 0.404 / 0.257 / 0.312 /
0.295 / 0.069. Across 200 random 35-response subsets (3-judge grain) κ(Novelty) ranges
**0.16–0.71** (median 0.39): the published 0.68 is an upper-tail draw of an unstable
subset estimate, and at full data the four core dimensions are statistically
indistinguishable in reliability (0.31–0.33), so "Novelty was the only dimension with good
agreement" fails.

**Replacement (Table 1 and all κ citations):** report full-data κ with the rater structure
stated (9 raters: 0.33/0.32/0.32/0.31/0.17; 3 judge-rounds: 0.40/0.26/0.31/0.30/0.07), label
Novelty "fair-to-moderate", and re-justify the Novelty focus on theoretical grounds (or add
human raters) rather than on reliability alone. §5.1.4 and the abstract sentence
"(Fleiss' κ = 0.68)" must change accordingly.

## 5. Post-hoc power (§4.5.1, Table 13)

**Problem.** Mean power 0.771 / 71.4% ≥ 0.8 reproduces exactly at the rating grain, i.e. it
inherits the inflation. Response grain: **mean power 0.544, 38.1% of comparisons ≥ 0.80**
(per-combination values in `recompute/power_response.csv`; e.g. Claude C5 1.00 and
DeepSeek C5 0.997 stay high, but Claude CE 0.507, GPT C11 0.369, Llama C5 0.479,
Gemini CE 0.083 do not).

**Replacement:** Table 13 from `power_response.csv`; §4.5.1 must state that most
comparisons are underpowered at the correct unit, which is why corrected CIs in §1 widen.

## 6. Pure persona effects and FDR stars (Table 17, §3.7.2)

**Problem.** The five published stars match no grain. BH-FDR on Welch t-tests at the paper's
own rating grain marks **16/21** significant (all except Claude C11, Mistral CE, Qwen C11,
Gemini C5, Gemini CE) — Claude C5 (d = 0.922, p ≈ 2e−76) is published *without* a star while
Qwen CE (d = 0.165) carries one. Response grain: **9/21** significant — Claude C5, DeepSeek
C5, GPT C5, Llama C5, Llama C11, Mistral C5, Mistral C11, Qwen C5, Gemini C11
(`recompute/pure_persona_fdr_response.csv`). Also, the closing sentence ("larger effect
sizes here … reflect the weaker baseline") is false for DeepSeek (0.379 < 0.581) and GPT
(0.395 < 0.501), whose small baselines outscore their large baselines.

**Replacement:** republish Table 17 with the response-grain d, p, p_FDR and stars; delete or
invert the "weaker baseline" sentence (sign and size differences vs Table 3 are driven by
which baseline each family's small model happens to beat).

## 7. Descriptive claims (§4.1.1)

- "DeepSeek showed the largest improvement from personas … +0.71 points (+26.9%)" → false at
  both grains. Largest improvement is **Claude + Culture_5: +0.97 points (+34.2%)**
  (response grain; rating grain +0.99 / +35.1%). DeepSeek is second.
- "Claude achieved the highest Novelty scores across all conditions (M = 3.14, SD = 1.22)":
  at the rating grain Qwen's Large Baseline (2.83) exceeds Claude's (2.82); at the response
  grain Claude leads (2.84 vs 2.83) but the quoted M/SD are single cells (Culture_Expert
  mean; Large-Baseline SD). Claude's overall response-grain mean is **3.10 (SD 1.05)**.
  Rewrite: "Claude achieved the highest mean Novelty in three of four conditions
  (M = 3.10, SD = 1.05 across conditions); Qwen's unsteered large model matched it."
- §4.1.2 "Gemini shows negligible effects across all personas (all |d| < 0.3)" vs the same
  subsection's "Culture_11 showing a small negative effect (d = −0.286)" and Table 3's
  "Small" label: at the response grain Gemini C11 is **−0.443 [−0.701, −0.182], medium**.
  Unify on one magnitude scheme (negligible < 0.2, small 0.2–0.5, medium 0.5–0.8,
  large ≥ 0.8) and apply it in text and tables.

## 8. Economic analysis (§4.4, Tables 7–8, 10, abstract, contributions)

- "Eight model-persona combinations" vs nine rows in Table 7, three of which (DeepSeek) have
  0% savings and so are not "lower cost". State the rule and count.
- Table 8's stated rule ("all combinations that achieved positive performance gains") is
  violated both ways: it includes non-significant Claude C11 (d = 0.056) and DeepSeek C11
  (0.006) while excluding positive Llama C5 (0.271, 77% savings, EGR 4.82), Llama CE (0.076,
  EGR 4.51), Mistral C5 (0.186), Gemini C5/CE. Under a CI-significance rule the qualifying
  set with cost savings is exactly six: **Claude C5, Claude CE, DeepSeek C5, DeepSeek CE,
  GPT C5, GPT CE**. Republish Tables 7–8 with one stated rule.
- EGR at response-grain means: GPT 9.15 / 8.53 / 8.18; Claude 2.24 / 1.84 / 1.70;
  DeepSeek 1.27 / 1.19 / 1.00 (paper: 9.17 / 8.53 / 8.18; 2.25 / 1.85 / 1.70; same DeepSeek).
- **EGR scale-dependence, now demonstrated from the data:** significantly *harmful*
  combinations score "exceptional/strong" EGR because the metric ratios 1–5 scale means
  against price ratios: Gemini C11 (d = −0.443, sig.) EGR **6.85**; Qwen C11 (d = −0.638,
  sig.) EGR **3.99**; Llama C11 (d = −0.412, sig.) EGR 3.78. Restrict EGR to combinations
  with CI-significant positive gains, or replace it with gain-per-dollar on a defined
  performance difference; add the assumption that output token counts are equal across
  models (Gemini's reasoning traces violate it).
- "40–88% lower cost" (abstract, contribution 4) → **40–87%** among defensible combinations;
  88% is Gemini's price ratio, and Gemini is excluded everywhere else as non-comparable.
  §4.4.4/§5.2.3/Table 9 already say 40–87% — align the abstract and intro.
- "GPT with Culture_5 … similar performance at 36× lower cost ($2.00 vs. $25.00)" →
  **12.5×** (25/2). The 60× figure for DeepSeek ($0.42 vs $25.00 = 59.5×) is correct.
- Table 10 "Avoid at all costs … −0.519 to −0.118": at the response grain the significant
  harms are Qwen C11 (−0.638), Mistral C11 (−0.496), Gemini C11 (−0.443), Llama C11
  (−0.412), Qwen CE (−0.365); the range and the "all models" wording need updating
  (Culture_11 is not significantly harmful for Claude, DeepSeek or GPT).

## 9. Gemini handling (§4.7 vs §4.2, §4.3)

Keep the anomaly disclosure, and add its consequences: Gemini enters the ANOVA, the
moderation test and the MDS "regional clustering" narrative despite being declared a
measurement artifact; at the response grain its Culture_11 effect is significant and
medium-sized. Domain-pooled effects without Gemini (`d_response_noGemini` in
`recompute/domain_effects.csv`): Culture_5 0.287 / 0.732 / 0.240 / 0.647 (Creative / GK /
Instruction / Reasoning) — the GK-and-Reasoning ordering is robust, so §4.3's claim survives
Gemini's exclusion; state the exclusion explicitly. Figure 3's "Eastern models form a
separate cluster" contradicts the figure (DeepSeek sits inside the Claude/GPT region);
rewrite as performance-profile similarity, not regional clustering.

## 10. Housekeeping (verified or confirmed from files)

- §3.1 "conducted in March 2025" vs model IDs (`gpt-5.4-2026-03-05`, claude-opus-4-6,
  gemini-3.1-pro-preview) → **March 2026**.
- §3.6.1 "temperature = 0.2 to ensure … deterministic scoring" → 0.2 is not deterministic.
- §3.6.2 "Each judge evaluated all responses" vs §3.6.3 κ on "a subset of 35 responses
  evaluated by all three judges" → all responses have all three judges; explain the subset.
- §3.7.2 "BH correction applied to all multiple comparisons" but Table 3 uses bootstrap-CI
  exclusion → say where FDR is and is not used.
- GPT Culture_5 n = 1,063 ratings = **120 responses** (20 extra problems) — explain or trim
  to the 100-problem set; it changes that cell's weight in every pooled statistic.
- Table 2/Figure 1 omit Small_Baseline although §4.1.1 promises all five conditions;
  Table 17's baseline means (small model) appear nowhere else — label them.
- Figure 1 caption's red/blue region coloring belongs to Figures 2–3.
- §4.5.3: Isolation Forest with contamination = 0.1 cannot flag 5.1%; re-run or restate.
- Repo hygiene: remove `.DS_Store`; the public CSV should carry the judge column for
  openai/gemini rows (currently only recoverable from `custom_id`).

## 11. What survives correction

The descriptive core is solid: response-grain means reproduce Table 2 within ±0.02; the
contingency pattern (Claude/DeepSeek benefit, Qwen/Mistral harmed by Culture_11, Gemini
inert-to-negative) holds with corrected CIs; domain ordering (Culture_5 strongest on General
Knowledge and Reasoning; Culture_11 negative in all four domains) holds with and without
Gemini; EGR arithmetic is internally correct; leave-one-out and mean/median robustness checks
are unaffected by grain. What changes is the inferential layer: fewer significant
comparisons (11/21 vs 15/21), no regional moderation, fair-to-moderate rather than good
judge agreement, underpowered post-hoc power, and a smaller, rule-consistent economic table.
