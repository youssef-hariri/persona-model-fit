#!/usr/bin/env python3
"""Apply the audited corrections (FIXES_PROPOSAL.md) to paper4_to_fix.tex,
producing paper4_v2_corrected.tex. Every replacement is an exact-match pair;
the script FAILS LOUDLY if any anchor is not found exactly once, so a changed
source file can never silently skip a fix. Re-runnable and diff-auditable.

Usage: venv/bin/python apply_fixes.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "paper" / "paper4_original_overleaf.tex"
DST = ROOT / "paper" / "paper4_v2_corrected.tex"

R = []  # (old, new) exact pairs

def rep(old, new):
    R.append((old, new))

# ============ TITLE / DATE ============
rep(r"\date{April 12 2026}", r"\date{September 25, 2026 (revised)}")

# ============ ABSTRACT ============
rep("we analyze over 25,000 responses using a multi-judge evaluation framework.",
    "we analyze 31,605 judge ratings of 3,516 model responses using a multi-judge "
    "evaluation framework, treating the response (the mean of its nine judge ratings) "
    "as the unit of analysis.")

rep("""Inter-rater reliability analysis revealed that Novelty was the only dimension with good agreement among judges (Fleiss' \\(\\kappa = 0.68\\)), justifying our focused analysis. Persona effectiveness follows a contingency model rather than a universal rule: effects are highly model-dependent. Claude with Culture\\_5 showed a large positive effect on Novelty (\\(d = 0.908\\)), while Qwen with Culture\\_11 showed a medium negative effect (\\(d = -0.519\\)). Domain-specific analysis revealed that Culture\\_5 performed best on General Knowledge (\\(d = 0.495\\)) and Reasoning (\\(d = 0.453\\)), while Culture\\_11 consistently harmed Novelty across all domains (\\(d = -0.170\\) to \\(-0.198\\)).""",
    """Inter-rater reliability over the full dataset was fair-to-moderate for all four core creativity dimensions (Fleiss' \\(\\kappa = 0.31\\)--\\(0.33\\)); we focus on Novelty as the construct central to our research question. Persona effectiveness follows a contingency model rather than a universal rule: effects are highly model-dependent. Claude with Culture\\_5 showed a large positive effect on Novelty (\\(d = 1.087\\)), while Qwen with Culture\\_11 showed a medium negative effect (\\(d = -0.638\\)); 11 of 21 model-persona comparisons reached statistical significance. Domain-specific analysis revealed that Culture\\_5 performed best on General Knowledge (\\(d = 0.628\\)) and Reasoning (\\(d = 0.545\\)), while Culture\\_11 harmed Novelty across all domains (\\(d = -0.149\\) to \\(-0.229\\)).""")

rep("""Economically, small models with personas achieved superior performance at 40-88\\% lower cost. The Efficiency Gain Ratio (EGR) provides a unified metric: GPT combinations achieved exceptional economic value (EGR up to 9.17, where EGR > 5 indicates exceptional value). Evidence for regional moderation was weak (Bayes Factor \\(= 0.331\\)), suggesting training origin may be less important than architectural factors.""",
    """Economically, six model-persona combinations achieved significant performance gains at 40-87\\% lower cost. The Efficiency Gain Ratio (EGR) provides a unified metric: GPT combinations achieved exceptional economic value (EGR up to 9.15, where EGR > 5 indicates exceptional value). Training region did not moderate persona effects (interaction \\(p = 0.445\\); Bayes Factor \\(= 0.331\\)), suggesting training origin is less important than architectural factors.""")

# ============ CONTRIBUTIONS ============
rep("Third, we demonstrate that inter-rater reliability varies substantially across creativity dimensions, with Novelty showing good agreement (\\(\\kappa = 0.68\\)) while other dimensions show poor to fair agreement, justifying a focused analysis on Novelty.",
    "Third, we demonstrate that inter-rater reliability is fair-to-moderate and statistically indistinguishable across the four core creativity dimensions (\\(\\kappa = 0.31\\)--\\(0.33\\)) when computed over the full dataset, motivating a theory-driven focus on Novelty with the remaining dimensions reported as exploratory.")
rep("Fourth, we introduce the Efficiency Gain Ratio (EGR) as a unified metric for cost-performance evaluation, demonstrating that small models with personas achieve superior performance at 40-88\\% lower cost, with GPT combinations achieving exceptional economic value (EGR up to 9.17).",
    "Fourth, we introduce the Efficiency Gain Ratio (EGR) as a unified metric for cost-performance evaluation, demonstrating that small models with personas achieve significant performance gains at 40-87\\% lower cost, with GPT combinations achieving exceptional economic value (EGR up to 9.15).")

# ============ LIT REVIEW: EGR placeholder citation ============
rep("An $EGR > 1.0$ indicates economic value; $EGR > 2.0$ indicates strong value; $EGR > 5.0$ indicates exceptional value; $EGR > 10.0$ indicates transformative value (\\cite{your_name_5e6c21fb}).",
    "An $EGR > 1.0$ indicates economic value; $EGR > 2.0$ indicates strong value; $EGR > 5.0$ indicates exceptional value; $EGR > 10.0$ indicates transformative value (thresholds defined as heuristics for this study).")

# ============ METHODOLOGY ============
rep("we focus our primary analysis on Novelty, the only dimension with good agreement among judges. All experimental procedures were conducted in March 2025.",
    "we focus our primary analysis on Novelty, the dimension central to our research question (Section 3.6). All experimental procedures were conducted in March 2026.")

rep("reasoning traces affecting direct comparability (see Section 4.6).",
    "reasoning traces affecting direct comparability (see Section 4.7).")

rep("All judges used temperature $= 0.2$ to ensure consistent, deterministic scoring, following established practice for evaluation tasks",
    "All judges used temperature $= 0.2$ to reduce variance in scoring, following established practice for evaluation tasks")

rep("""To assess the consistency of the three judge models, we calculated Fleiss' Kappa (\\(\\kappa\\)) for each of the five creativity dimensions using a subset of 35 responses evaluated by all three judges. Fleiss' Kappa measures the level of agreement between multiple raters beyond chance, with values interpreted as: \\(\\kappa < 0.20\\) poor, \\(0.20 \\leq \\kappa < 0.40\\) fair, \\(0.40 \\leq \\kappa < 0.60\\) moderate, \\(0.60 \\leq \\kappa < 0.75\\) good, and \\(\\kappa \\geq 0.75\\) excellent.

As shown in Table~\\ref{tab:inter_rater}), the dimensions exhibited varying levels of agreement:""",
    """Every response was evaluated by all three judges under all three prompt variations (nine ratings per response), so reliability can be estimated on the full dataset rather than on a subset. We calculated Fleiss' Kappa (\\(\\kappa\\)) for each of the five creativity dimensions over all 3,516 responses, both at the level of the nine individual ratings per response and at the level of the three judge-level mean ratings. Fleiss' Kappa measures the level of agreement between multiple raters beyond chance, with values interpreted as: \\(\\kappa < 0.20\\) poor, \\(0.20 \\leq \\kappa < 0.40\\) fair, \\(0.40 \\leq \\kappa < 0.60\\) moderate, \\(0.60 \\leq \\kappa < 0.75\\) good, and \\(\\kappa \\geq 0.75\\) excellent.

As shown in Table~\\ref{tab:inter_rater}, the dimensions exhibited similar levels of agreement:""")

rep("""\\begin{tabular}{lcc}
\\toprule
\\textbf{Dimension} & \\textbf{Fleiss' \\(\\kappa\\)} & \\textbf{Interpretation} \\\\
\\midrule
Novelty & 0.68 & Good \\\\
Usefulness & 0.15 & Poor \\\\
Flexibility & 0.30 & Fair \\\\
Elaboration & 0.30 & Fair \\\\
Cultural Sensitivity & -0.23 & Poor \\\\
\\bottomrule
\\end{tabular}
\\caption*{\\footnotesize Based on 35 responses evaluated by three judge models. \\(\\kappa < 0.20\\) = poor, \\(0.20-0.40\\) = fair, \\(0.40-0.60\\) = moderate, \\(0.60-0.75\\) = good, \\(>0.75\\) = excellent. \\textbf{Note:} Cultural Sensitivity shows negative \\(\\kappa = -0.23\\), indicating systematic disagreement among judges worse than chance. This suggests the dimension may be too subjective for reliable LLM-based evaluation.}""",
    """\\begin{tabular}{lccc}
\\toprule
\\textbf{Dimension} & \\(\\kappa\\) (9 ratings) & \\(\\kappa\\) (3 judge means) & \\textbf{Interpretation} \\\\
\\midrule
Novelty & 0.33 & 0.40 & Fair--moderate \\\\
Usefulness & 0.32 & 0.26 & Fair \\\\
Flexibility & 0.32 & 0.31 & Fair \\\\
Elaboration & 0.31 & 0.30 & Fair \\\\
Cultural Sensitivity & 0.17 & 0.07 & Poor \\\\
\\bottomrule
\\end{tabular}
\\caption*{\\footnotesize Computed over all 3,516 responses, each rated by three judges under three prompt variations. ``9 ratings'' treats each judge $\\times$ variation score as a separate rating; ``3 judge means'' averages variations within judge. \\(\\kappa < 0.20\\) = poor, \\(0.20-0.40\\) = fair, \\(0.40-0.60\\) = moderate. \\textbf{Note:} Cultural Sensitivity shows the lowest agreement (\\(\\kappa = 0.17\\)), suggesting the dimension may be too subjective for reliable LLM-based evaluation.}""")

rep("""Novelty was the only dimension with good inter-rater agreement (\\(\\kappa = 0.68\\)). Consequently, we focus our primary analysis on Novelty, treating findings from other dimensions as exploratory given their lower reliability.""",
    """Agreement was fair-to-moderate for the four core creativity dimensions (\\(\\kappa = 0.31\\)--\\(0.33\\), statistically indistinguishable from one another) and poor for Cultural Sensitivity. An earlier subset-based estimate (\\(\\kappa = 0.68\\) for Novelty, 35 responses) proved unstable---across random 35-response subsets \\(\\kappa\\) for Novelty ranges from 0.16 to 0.71 (median 0.39)---so we report full-data values throughout. Because reliability does not privilege any single core dimension, our focus on Novelty is theoretical: it is the construct at the center of our research question. Findings for the other dimensions are reported as exploratory given their limited reliability.""")

rep("Effect sizes were interpreted as small ($|d| < 0.5$), medium ($0.5 \\le |d| < 0.8$), or large ($|d| \\ge 0.8$).",
    "Effect sizes were interpreted as negligible ($|d| < 0.2$), small ($0.2 \\le |d| < 0.5$), medium ($0.5 \\le |d| < 0.8$), or large ($|d| \\ge 0.8$).")

rep("""\\begin{itemize}
    \\item \\textbf{Two-Way ANOVA:} Used to test Persona $\\times$ Model Family interactions for Novelty.
    \\item \\textbf{Moderation Analysis:} Tested whether training region (Eastern vs. Western) moderates persona effects using OLS regression, with Bayes Factor calculated to quantify evidence strength (Rouder et al., 2009).
    \\item \\textbf{Domain Analysis:} Calculated effect sizes for each persona across the four problem domains.
    \\item \\textbf{False Discovery Rate (FDR):} Benjamini-Hochberg correction applied to all multiple comparisons.
\\end{itemize}""",
    """\\begin{itemize}
    \\item \\textbf{Unit of Analysis:} All inferential statistics treat the response (the mean of its nine judge ratings) as the unit of analysis ($N = 3{,}516$ responses; approximately 100 per model $\\times$ condition cell). Judge and prompt variation are within-response replications, not independent observations.
    \\item \\textbf{Two-Way ANOVA:} Used to test Persona $\\times$ Region interactions for Novelty.
    \\item \\textbf{Moderation Analysis:} Tested whether training region (Eastern vs. Western) moderates persona effects using OLS regression, with Bayes Factor calculated to quantify evidence strength (Rouder et al., 2009).
    \\item \\textbf{Domain Analysis:} Calculated effect sizes for each persona across the four problem domains.
    \\item \\textbf{False Discovery Rate (FDR):} Benjamini-Hochberg correction applied to the family of pure persona effect tests (Appendix A.8); significance elsewhere is assessed by bootstrap confidence-interval exclusion.
\\end{itemize}""")

rep("""    The performance value is the Novelty score.
    Thresholds: $EGR > 1.0 =$ economic value, $EGR > 2.0 =$ strong value, $EGR > 5.0 =$ exceptional value, $EGR > 10.0 =$ transformative value.""",
    """    The performance value is the Novelty score.
    Thresholds: $EGR > 1.0 =$ economic value, $EGR > 2.0 =$ strong value, $EGR > 5.0 =$ exceptional value, $EGR > 10.0 =$ transformative value.
    The metric assumes comparable output token counts across models; Gemini's reasoning traces violate this assumption (Section 4.7), so Gemini is excluded from the economic analysis. Because EGR ratios a 1--5 scale mean against a price ratio, it can label significantly \\emph{harmful} combinations as valuable (e.g., Qwen with Culture\\_11, $d = -0.638$, would score EGR $= 3.99$); we therefore report EGR only for combinations with statistically significant positive gains.""")

rep("""    \\item \\textbf{ANOVA Assumptions:} Shapiro-Wilk test for normality of residuals; Levene's test for homogeneity of variance.
\\end{itemize}""",
    """    \\item \\textbf{ANOVA Assumptions:} Shapiro-Wilk test for normality of residuals; Levene's test for homogeneity of variance (results reported in Section 4.2.1).
\\end{itemize}""")

# ============ RESULTS: opening ============
rep("""Based on the inter-rater reliability analysis (Section 3.6), which showed that Novelty was the only dimension with good agreement among judges (\\(\\kappa = 0.68\\)), we focus our primary analysis on Novelty. Findings for Usefulness, Flexibility, Elaboration, and Cultural Sensitivity are reported in the Appendix due to their lower reliability.""",
    """Based on the inter-rater reliability analysis (Section 3.6), which showed fair-to-moderate agreement for the four core dimensions (\\(\\kappa = 0.31\\)--\\(0.33\\)) and poor agreement for Cultural Sensitivity (\\(\\kappa = 0.17\\)), we focus our primary analysis on Novelty, the dimension central to our research question. Findings for Usefulness, Flexibility, Elaboration, and Cultural Sensitivity are reported in the Appendix as exploratory.""")

# ============ 4.1.1 Table 2 + text ============
rep("Table~\\ref{tab:means_novelty} presents the mean Novelty scores (1-5 scale) for each model-condition combination.",
    "Table~\\ref{tab:means_novelty} presents the mean Novelty scores (1-5 scale) for the three persona conditions and the large baseline (Small Baseline means appear in Appendix A.8). Standard deviations and sample sizes are reported at the response level, the unit of all inferential analyses in this paper.")

rep("""Claude & 3.81 (0.88) & 3.14 (1.22) & 2.89 (1.12) & 2.82 (1.26) \\\\
Gemini & 1.49 (0.98) & 1.45 (0.86) & 1.21 (0.55) & 1.41 (0.85) \\\\
GPT & 3.23 (1.13) & 3.00 (1.19) & 2.88 (1.16) & 2.64 (1.22) \\\\
Llama & 2.50 (1.03) & 2.35 (0.95) & 1.97 (0.93) & 2.29 (1.06) \\\\
Mistral & 2.50 (1.05) & 2.30 (0.99) & 1.95 (0.99) & 2.36 (1.06) \\\\
\\midrule
\\textbf{Eastern Models} \\\\
DeepSeek & 3.35 (1.15) & 3.13 (1.18) & 2.64 (1.16) & 2.64 (1.28) \\\\
Qwen & 2.63 (0.99) & 2.51 (0.94) & 2.26 (0.99) & 2.83 (1.23) \\\\""",
    """Claude & 3.81 (0.64) & 3.14 (1.06) & 2.89 (0.95) & 2.84 (1.09) \\\\
Gemini & 1.49 (0.73) & 1.45 (0.56) & 1.21 (0.34) & 1.41 (0.55) \\\\
GPT & 3.22 (0.99) & 3.00 (1.04) & 2.88 (1.02) & 2.64 (1.06) \\\\
Llama & 2.50 (0.74) & 2.34 (0.68) & 1.97 (0.68) & 2.29 (0.86) \\\\
Mistral & 2.50 (0.74) & 2.29 (0.74) & 1.95 (0.80) & 2.36 (0.85) \\\\
\\midrule
\\textbf{Eastern Models} \\\\
DeepSeek & 3.35 (1.02) & 3.14 (1.03) & 2.64 (1.00) & 2.64 (1.13) \\\\
Qwen & 2.63 (0.71) & 2.51 (0.69) & 2.26 (0.72) & 2.83 (1.05) \\\\""")

rep("""\\caption*{\\footnotesize Standard deviations in parentheses. n = 900 per condition except: GPT Culture\\_5 = 1,063; DeepSeek Large Baseline = 884. \\textbf{Note:} Gemini shows notably smaller standard deviations (e.g., 0.55 for Culture\\_11 vs. 0.88-1.28 for others), indicating consistently low scores with little variation across responses.}""",
    """\\caption*{\\footnotesize Response-level means and standard deviations (each response is the mean of nine judge ratings). n = 100 responses per cell except GPT Culture\\_5 = 120 (20 of the 100 problems were generated twice; averaging duplicates to one value per problem leaves the conclusion unchanged, $d = 0.624$ vs. $0.570$) and Gemini/Mistral Large Baseline = 99. \\textbf{Note:} Gemini shows notably smaller standard deviations (e.g., 0.34 for Culture\\_11 vs. 0.64--1.13 for others), indicating consistently low scores with little variation across responses.}""")

rep("""\\caption{Mean Novelty scores by model and condition. Error bars represent $\\pm1$ standard deviation. Eastern models (DeepSeek, Qwen) shown in red; Western models in blue.}""",
    """\\caption{Mean Novelty scores by model and condition. Error bars represent $\\pm1$ standard deviation (response level). Bars are colored by condition; models are grouped by training region (Eastern: DeepSeek, Qwen; Western: the remaining five), separated by the dotted line.}""")

rep("""Claude achieved the highest Novelty scores across all conditions ($M = 3.14$, $SD = 1.22$), consistently outperforming other models. Gemini performed substantially lower ($M = 1.39$, $SD = 0.87$), with scores approximately 1.8 points below the next lowest model. DeepSeek showed the largest improvement from personas, with Culture\\_5 outperforming its baseline by 0.71 points ($+26.9\\%$). In contrast, Qwen showed the largest degradation with Culture\\_11, dropping 0.57 points ($-20.1\\%$) below baseline.""",
    """Claude achieved the highest mean Novelty in three of four conditions ($M = 3.10$, $SD = 1.05$ across conditions); Qwen's unsteered large model matched it ($2.83$ vs. $2.84$). Gemini performed substantially lower ($M = 1.39$ across conditions), approximately 0.9 points below the next-lowest models (Llama and Mistral, both $M = 2.28$). Claude showed the largest improvement from personas, with Culture\\_5 outperforming its large baseline by 0.97 points ($+34.2\\%$); DeepSeek showed the second-largest improvement ($+0.71$ points, $+27.1\\%$). In contrast, Qwen showed the largest degradation with Culture\\_11, dropping 0.58 points ($-20.3\\%$) below baseline.""")

# ============ 4.1.2 intro + Table 3 + patterns ============
rep("""To quantify the practical significance of persona effects, we calculated Cohen's $d$ effect sizes comparing each persona to the large baseline, with 95\\% bootstrap confidence intervals (5,000 resamples). Positive values indicate improvement over baseline; negative values indicate degradation. Effect sizes are interpreted as small ($|d| < 0.5$), medium ($0.5 \\le |d| < 0.8$), or large ($|d| \\ge 0.8$).""",
    """To quantify the practical significance of persona effects, we calculated Cohen's $d$ effect sizes comparing each persona to the large baseline at the response level (100 responses per cell), with 95\\% bootstrap confidence intervals (5,000 resamples). Positive values indicate improvement over baseline; negative values indicate degradation. Effect sizes are interpreted as negligible ($|d| < 0.2$), small ($0.2 \\le |d| < 0.5$), medium ($0.5 \\le |d| < 0.8$), or large ($|d| \\ge 0.8$).""")

rep("""Claude & Culture\\_5 & 0.908 & [0.806, 1.013] & Large \\\\
Claude & Culture\\_Expert & 0.252 & [0.159, 0.349] & Small \\\\
Claude & Culture\\_11 & 0.052 & [-0.041, 0.141] & Negligible \\\\
DeepSeek & Culture\\_5 & 0.581 & [0.484, 0.684] & Medium \\\\
DeepSeek & Culture\\_Expert & 0.402 & [0.300, 0.501] & Small \\\\
DeepSeek & Culture\\_11 & 0.003 & [-0.089, 0.094] & Negligible \\\\
GPT & Culture\\_5 & 0.501 & [0.416, 0.595] & Medium \\\\
GPT & Culture\\_Expert & 0.301 & [0.210, 0.399] & Small \\\\
GPT & Culture\\_11 & 0.202 & [0.112, 0.298] & Small \\\\
Llama & Culture\\_5 & 0.209 & [0.123, 0.298] & Small \\\\
Llama & Culture\\_Expert & 0.059 & [-0.030, 0.150] & Negligible \\\\
Llama & Culture\\_11 & -0.321 & [-0.415, -0.229] & Small \\\\
Mistral & Culture\\_5 & 0.141 & [0.051, 0.232] & Negligible \\\\
Mistral & Culture\\_Expert & -0.060 & [-0.152, 0.033] & Negligible \\\\
Mistral & Culture\\_11 & -0.399 & [-0.491, -0.307] & Small \\\\
Qwen & Culture\\_5 & -0.185 & [-0.275, -0.091] & Negligible \\\\
Qwen & Culture\\_Expert & -0.297 & [-0.387, -0.207] & Small \\\\
Qwen & Culture\\_11 & -0.519 & [-0.611, -0.424] & Medium \\\\
Gemini & Culture\\_5 & 0.091 & [-0.005, 0.182] & Negligible \\\\
Gemini & Culture\\_Expert & 0.049 & [-0.043, 0.142] & Negligible \\\\
Gemini & Culture\\_11 & -0.286 & [-0.369, -0.195] & Small \\\\""",
    """Claude & Culture\\_5 & 1.087 & [0.800, 1.417] & Large \\\\
Claude & Culture\\_Expert & 0.281 & [0.012, 0.574] & Small \\\\
Claude & Culture\\_11 & 0.056 & [-0.213, 0.337] & Negligible \\\\
DeepSeek & Culture\\_5 & 0.664 & [0.384, 0.993] & Medium \\\\
DeepSeek & Culture\\_Expert & 0.464 & [0.186, 0.770] & Small \\\\
DeepSeek & Culture\\_11 & 0.006 & [-0.264, 0.285] & Negligible \\\\
GPT & Culture\\_5 & 0.570 & [0.308, 0.868] & Medium \\\\
GPT & Culture\\_Expert & 0.344 & [0.070, 0.647] & Small \\\\
GPT & Culture\\_11 & 0.231 & [-0.043, 0.521] & Small \\\\
Llama & Culture\\_5 & 0.271 & [-0.006, 0.561] & Small \\\\
Llama & Culture\\_Expert & 0.076 & [-0.196, 0.363] & Negligible \\\\
Llama & Culture\\_11 & -0.412 & [-0.693, -0.131] & Small \\\\
Mistral & Culture\\_5 & 0.186 & [-0.094, 0.461] & Negligible \\\\
Mistral & Culture\\_Expert & -0.077 & [-0.367, 0.203] & Negligible \\\\
Mistral & Culture\\_11 & -0.496 & [-0.816, -0.215] & Small \\\\
Qwen & Culture\\_5 & -0.229 & [-0.504, 0.040] & Small \\\\
Qwen & Culture\\_Expert & -0.365 & [-0.642, -0.097] & Small \\\\
Qwen & Culture\\_11 & -0.638 & [-0.925, -0.366] & Medium \\\\
Gemini & Culture\\_5 & 0.131 & [-0.154, 0.396] & Negligible \\\\
Gemini & Culture\\_Expert & 0.076 & [-0.205, 0.355] & Negligible \\\\
Gemini & Culture\\_11 & -0.443 & [-0.701, -0.182] & Small \\\\""")

rep("""\\caption*{\\footnotesize Magnitude: negligible ($|d| < 0.2$), small ($0.2 \\le |d| < 0.5$), medium ($0.5 \\le |d| < 0.8$), large ($|d| \\ge 0.8$). Bootstrap confidence intervals (5,000 resamples) that do not contain zero indicate statistical significance (15/21 comparisons).}""",
    """\\caption*{\\footnotesize Response-level effect sizes (each response is the mean of nine judge ratings). Magnitude: negligible ($|d| < 0.2$), small ($0.2 \\le |d| < 0.5$), medium ($0.5 \\le |d| < 0.8$), large ($|d| \\ge 0.8$). Bootstrap confidence intervals (5,000 resamples) that do not contain zero indicate statistical significance (11/21 comparisons).}""")

rep("""\\caption{Forest plot of Cohen's d effect sizes for Novelty with 95\\% confidence intervals. Red points indicate Eastern models (DeepSeek, Qwen); blue points indicate Western models. The vertical dashed line represents no effect.}""",
    """\\caption{Forest plot of response-level Cohen's d effect sizes for Novelty with 95\\% bootstrap confidence intervals. Red points indicate Eastern models (DeepSeek, Qwen); blue points indicate Western models; crosses mark intervals that include zero (non-significant). The vertical dashed line represents no effect.}""")

rep("""\\textbf{Consistently Positive:} Claude and DeepSeek show positive effects across most personas. Claude with Culture\\_5 achieves a large positive effect ($d = 0.908$), the largest in the study. DeepSeek with Culture\\_5 shows a medium positive effect ($d = 0.581$). GPT shows modest positive effects across all personas ($d = 0.202$ to $0.501$).

\\textbf{Consistently Negative:} Qwen shows negative effects across all personas, with Culture\\_11 showing a medium negative effect ($d = -0.519$). Mistral shows mixed but predominantly negative effects, with Culture\\_11 showing a small-to-medium negative effect ($d = -0.399$).

\\textbf{Neutral or Mixed:} Llama shows a small positive effect for Culture\\_5 ($d = 0.209$) but a small negative effect for Culture\\_11 ($d = -0.321$). Gemini shows negligible effects across all personas (all $|d| < 0.3$), with only Culture\\_11 showing a small negative effect ($d = -0.286$).""",
    """\\textbf{Consistently Positive:} Claude and DeepSeek show positive effects across most personas. Claude with Culture\\_5 achieves a large positive effect ($d = 1.087$), the largest in the study. DeepSeek with Culture\\_5 shows a medium positive effect ($d = 0.664$). GPT shows significant small-to-medium positive effects for Culture\\_5 ($d = 0.570$) and Culture\\_Expert ($d = 0.344$); its Culture\\_11 effect is not significant ($d = 0.231$, CI includes zero).

\\textbf{Consistently Negative:} Qwen shows negative effects across all personas, significant for Culture\\_Expert ($d = -0.365$) and for Culture\\_11 ($d = -0.638$, medium). Mistral shows mixed but predominantly negative effects, with Culture\\_11 showing a significant small negative effect ($d = -0.496$).

\\textbf{Neutral or Mixed:} Llama shows a non-significant small positive effect for Culture\\_5 ($d = 0.271$) but a significant small negative effect for Culture\\_11 ($d = -0.412$). Gemini shows negligible, non-significant effects for Culture\\_5 and Culture\\_Expert ($|d| < 0.14$); its Culture\\_11 effect is negative and significant ($d = -0.443$), although Gemini's results carry the measurement caveat of Section 4.7.""")

rep("""Persona effectiveness on Novelty is not universal. Claude and DeepSeek benefit substantially; Qwen and Mistral are harmed; Gemini shows negligible effects. This heterogeneity motivates our investigation of the factors that moderate persona effectiveness.""",
    """Persona effectiveness on Novelty is not universal. Claude and DeepSeek benefit substantially; Qwen and Mistral are harmed; Gemini is largely unresponsive, with a significant negative Culture\\_11 effect that should be read in light of its evaluation anomaly (Section 4.7). This heterogeneity motivates our investigation of the factors that moderate persona effectiveness.""")

# ============ 4.2.1 ANOVA ============
rep("""\\subsubsection{Two-Way ANOVA (Persona $\\times$ Model Family)}

A two-way ANOVA with persona (4 levels) and model family (2 levels: Eastern vs. Western) as fixed factors revealed a marginally significant interaction ($F(3, 25297) = 2.58$, $p = 0.052$), suggesting that persona effects may vary by model family, though the evidence is not conclusive at conventional thresholds. Table~\\ref{tab:anova_novelty} presents the full ANOVA results.""",
    """\\subsubsection{Two-Way ANOVA (Persona $\\times$ Region)}

A two-way ANOVA with persona (4 levels) and training region (2 levels: Eastern vs. Western) as fixed factors, computed at the response level, revealed strong main effects of persona and region but no interaction ($F(3, 2810) = 0.89$, $p = 0.445$), indicating that persona effects do not vary systematically by training region. Table~\\ref{tab:anova_novelty} presents the full ANOVA results. Assumption checks indicated non-normal residuals (Shapiro-Wilk $p < 0.001$) and heterogeneity of variance (Levene $p = 0.003$); with 2,818 observations the F-tests are robust to these violations, and the key inferences in this paper rely on bootstrap confidence intervals rather than ANOVA p-values.""")

rep("""\\caption{Two-Way ANOVA Results for Novelty (Persona $\\times$ Model Family)}""",
    """\\caption{Two-Way ANOVA Results for Novelty (Persona $\\times$ Region)}""")

rep("""Persona & 429.53 & 3 & 192.89 & $<$0.001 \\\\
Model Family & 664.17 & 1 & 894.77 & $<$0.001 \\\\
Persona $\\times$ Model Family & 5.74 & 3 & 2.58 & 0.052 \\\\
Residual & 18777.35 & 25297 & & \\\\""",
    """Persona & 112.31 & 3 & 35.75 & $<$0.001 \\\\
Region & 64.41 & 1 & 61.51 & $<$0.001 \\\\
Persona $\\times$ Region & 2.80 & 3 & 0.89 & 0.445 \\\\
Residual & 2942.46 & 2810 & & \\\\""")

rep("""\\caption*{\\footnotesize Marginally significant interaction suggests persona effects may depend on model architecture, though evidence is inconclusive.}""",
    """\\caption*{\\footnotesize Response-level analysis ($n = 2{,}818$ responses). No persona $\\times$ region interaction. An earlier version of this table, computed on a superseded data extract, reported a marginal interaction ($p = 0.052$) that matched neither the rating-level ($p = 0.0004$) nor the response-level ($p = 0.445$) analysis of the released data; it has been corrected.}""")

# ============ 4.2.2 Moderation ============
rep("""To test whether training region moderates persona effects, we conducted a moderation analysis with region (Eastern vs. Western) as the moderator. Results show a statistically significant moderation effect ($t = 2.08$, $p = 0.037$), indicating that Eastern models show greater responsiveness to cultural personas than Western models. However, the Bayes Factor ($BF = 0.331$) provides anecdotal evidence against the moderation hypothesis, indicating that the frequentist significance may be spurious. Table~\\ref{tab:moderation_novelty} presents the full moderation results.""",
    """To test whether training region moderates persona effects, we conducted a moderation analysis with region (Eastern vs. Western) as the moderator. At the response level, region did not moderate persona effects ($t = -1.27$, $p = 0.21$ for the persona $\\times$ region interaction), consistent with the Bayes Factor ($BF = 0.331$), which provides anecdotal evidence against the moderation hypothesis. Table~\\ref{tab:moderation_novelty} presents the full moderation results.""")

rep("""Constant & 2.304 & 0.018 & 126.93 & $<$0.001 \\\\
Is Eastern & 0.433 & 0.034 & 12.74 & $<$0.001 \\\\
Is Persona & 0.148 & 0.021 & 7.08 & $<$0.001 \\\\
Eastern $\\times$ Persona & -0.134 & 0.039 & -3.41 & 0.001 \\\\""",
    """Constant & 2.307 & 0.047 & 49.46 & $<$0.001 \\\\
Is Eastern & 0.428 & 0.087 & 4.91 & $<$0.001 \\\\
Is Persona & 0.147 & 0.054 & 2.73 & 0.006 \\\\
Eastern $\\times$ Persona & -0.127 & 0.101 & -1.27 & 0.206 \\\\""")

rep("""\\caption*{\\footnotesize Bayes Factor for interaction: $BF = 0.331$ (anecdotal evidence against moderation). Eastern models: DeepSeek, Qwen; Western models: Claude, Gemini, GPT, Llama, Mistral.}""",
    """\\caption*{\\footnotesize Response-level OLS ($n = 2{,}818$ responses). Bayes Factor for interaction: $BF = 0.331$ (anecdotal evidence against moderation). Eastern models: DeepSeek, Qwen; Western models: Claude, Gemini, GPT, Llama, Mistral.}""")

rep("""Quantitatively, Eastern models show stronger positive effects from Culture\\_Expert ($d = +0.144$) compared to Western models ($d = +0.023$), representing a sixfold difference in effect magnitude. For Culture\\_5, Eastern models show a smaller negative effect ($d = -0.049$) than Western models ($d = -0.064$). For Culture\\_11, both groups show similar negative effects ($d = -0.338$ for Eastern, $-0.345$ for Western), indicating that Culture\\_11's detrimental effect is region-invariant.""",
    """Descriptively, Western models show slightly larger mean effects for the positive personas (Culture\\_5: $d = +0.449$ Western vs. $+0.218$ Eastern; Culture\\_Expert: $+0.140$ vs. $+0.050$), while Culture\\_11 is negative in both regions ($-0.213$ Western, $-0.316$ Eastern); none of these differences is significant (Culture\\_Expert $\\times$ East: $t = 0.87$, $p = 0.38$; HC3-robust $p = 0.35$). The apparent significance of regional moderation at the rating level ($t = -3.41$ for the binary specification) is an artifact of treating the nine judge ratings of each response as independent observations, and an earlier report that Eastern models respond more strongly to Culture\\_Expert does not survive correction at either grain.""")

# ============ 4.2.3 MDS + 4.2.4 ============
rep("""The MDS analysis reveals that Western models (Claude, GPT, Llama, Mistral) cluster together, while Eastern models (DeepSeek, Qwen) form a separate cluster. Gemini is a notable outlier, positioned far from all other models, reflecting its uniquely low Novelty scores across all conditions.""",
    """The MDS analysis reveals clustering by performance profile rather than by training region: Claude, GPT, and DeepSeek form a high-Novelty group, while Llama, Mistral, and Qwen occupy a mid-range region. Gemini is a notable outlier, positioned far from all other models, reflecting its uniquely low Novelty scores across all conditions.""")

rep("""Persona effectiveness on Novelty depends on both model architecture and training region, though the evidence for regional moderation is weak (Bayes Factor = 0.331). Eastern models show greater responsiveness to cultural personas, particularly Culture\\_Expert, while Western models show mixed or muted responses.""",
    """Persona effectiveness on Novelty depends on model architecture but shows no evidence of regional moderation at the response level (interaction $p = 0.445$; Bayes Factor = 0.331). Earlier indications that Eastern models respond more strongly to cultural personas were artifacts of rating-level analysis.""")

# ============ 4.3 domains ============
rep("""Culture\\_5 & 0.207 & \\textbf{0.495} & 0.159 & 0.453 \\\\
Culture\\_Expert & 0.032 & 0.174 & 0.079 & \\textbf{0.175} \\\\
Culture\\_11 & -0.170 & -0.118 & -0.198 & -0.124 \\\\
\\bottomrule
\\end{tabular}
\\caption*{\\footnotesize Bold indicates largest effect for each persona. All Culture\\_11 effects are negative.}""",
    """Culture\\_5 & 0.233 & \\textbf{0.628} & 0.185 & 0.545 \\\\
Culture\\_Expert & 0.036 & \\textbf{0.223} & 0.092 & 0.210 \\\\
Culture\\_11 & -0.196 & -0.154 & -0.229 & -0.149 \\\\
\\bottomrule
\\end{tabular}
\\caption*{\\footnotesize Response-level effect sizes, models pooled. Bold indicates largest effect for each persona. All Culture\\_11 effects are negative. The pattern is unchanged when Gemini is excluded (Culture\\_5: $d = 0.287/0.732/0.240/0.647$ for Creative/General Knowledge/Instruction/Reasoning).}""")

rep("""\\textbf{Culture\\_5} performs best on General Knowledge problems ($d = 0.495$) and Reasoning problems ($d = 0.453$), with smaller effects on Creative ($d = 0.207$) and Instruction ($d = 0.159$).

\\textbf{Culture\\_Expert} shows small positive effects across all domains, with the largest effect on Reasoning ($d = 0.175$), followed closely by General Knowledge ($d = 0.174$).

\\textbf{Culture\\_11} consistently harms Novelty across all domains, with the most negative effect on Instruction ($d = -0.198$) and Creative ($d = -0.170$).""",
    """\\textbf{Culture\\_5} performs best on General Knowledge problems ($d = 0.628$) and Reasoning problems ($d = 0.545$), with smaller effects on Creative ($d = 0.233$) and Instruction ($d = 0.185$).

\\textbf{Culture\\_Expert} shows small positive effects across all domains, with the largest effect on General Knowledge ($d = 0.223$), followed closely by Reasoning ($d = 0.210$).

\\textbf{Culture\\_11} harms Novelty across all domains, with the most negative effect on Instruction ($d = -0.229$) and Creative ($d = -0.196$).""")

rep("""\\caption{Effect sizes (Cohen's d) for Novelty by persona and problem domain. Blue indicates negative effects (harmful), red indicates positive effects (beneficial).}""",
    """\\caption{Response-level effect sizes (Cohen's d) for Novelty by persona and problem domain, models pooled. Blue indicates negative effects (harmful), red indicates positive effects (beneficial).}""")

# ============ 4.4 Economics ============
rep("""Eight model-persona combinations demonstrate that small models with personas achieve superior or equivalent performance at significantly lower cost. Table~\\ref{tab:economics_novelty} presents the complete cost-performance landscape for Novelty.""",
    """Six model-persona combinations achieve statistically significant Novelty gains (95\\% bootstrap CI excludes zero) with small-model cost at or below their own large model's cost. Table~\\ref{tab:economics_novelty} presents the cost-performance landscape for these combinations.""")

rep("""GPT & Culture\\_5 & 0.501 & \\$2.00 & \\$15.00 & 87\\% \\\\
GPT & Culture\\_Expert & 0.301 & \\$2.00 & \\$15.00 & 87\\% \\\\
GPT & Culture\\_11 & 0.202 & \\$2.00 & \\$15.00 & 87\\% \\\\
Claude & Culture\\_5 & 0.908 & \\$15.00 & \\$25.00 & 40\\% \\\\
Claude & Culture\\_Expert & 0.252 & \\$15.00 & \\$25.00 & 40\\% \\\\
DeepSeek & Culture\\_5 & 0.581 & \\$0.42 & \\$0.42 & 0\\% \\\\
DeepSeek & Culture\\_Expert & 0.402 & \\$0.42 & \\$0.42 & 0\\% \\\\
DeepSeek & Culture\\_11 & 0.003 & \\$0.42 & \\$0.42 & 0\\% \\\\
\\bottomrule
\\end{tabular}
\\caption*{\\footnotesize Output token costs per 1M tokens. DeepSeek shows cost parity (identical small/large costs) but positive performance gains.}""",
    """GPT & Culture\\_5 & 0.570 & \\$2.00 & \\$15.00 & 87\\% \\\\
GPT & Culture\\_Expert & 0.344 & \\$2.00 & \\$15.00 & 87\\% \\\\
Claude & Culture\\_5 & 1.087 & \\$15.00 & \\$25.00 & 40\\% \\\\
Claude & Culture\\_Expert & 0.281 & \\$15.00 & \\$25.00 & 40\\% \\\\
DeepSeek & Culture\\_5 & 0.664 & \\$0.42 & \\$0.42 & 0\\% \\\\
DeepSeek & Culture\\_Expert & 0.464 & \\$0.42 & \\$0.42 & 0\\% \\\\
\\bottomrule
\\end{tabular}
\\caption*{\\footnotesize Output token costs per 1M tokens. Inclusion rule: statistically significant positive Novelty gain (Table~\\ref{tab:effects_complete}) and small-model cost $\\le$ large-model cost. DeepSeek shows cost parity (identical small/large costs) but significant positive performance gains.}""")

rep("""\\textbf{GPT combinations} achieve the best balance, delivering positive performance gains ($d = 0.202$ to $0.501$) with exceptional cost savings (87\\%), placing them firmly in the optimal region.

\\textbf{Claude with Culture\\_5} achieves the largest performance gain ($d = 0.908$) with substantial cost savings (40\\%), approaching the optimal region.

\\textbf{DeepSeek combinations} achieve positive performance gains ($d = 0.003$ to $0.581$) but offer no cost savings (0\\%), placing them in the high-performance, high-cost quadrant.""",
    """\\textbf{GPT combinations} achieve the best balance, delivering significant positive performance gains ($d = 0.344$ to $0.570$) with exceptional cost savings (87\\%), placing them firmly in the optimal region.

\\textbf{Claude with Culture\\_5} achieves the largest performance gain ($d = 1.087$) with substantial cost savings (40\\%), approaching the optimal region.

\\textbf{DeepSeek combinations} achieve significant positive performance gains ($d = 0.464$ to $0.664$) but offer no cost savings (0\\%), placing them in the high-performance, cost-parity quadrant.""")

rep("""Beyond within-family comparisons, small models with personas can outperform larger models from competing providers. DeepSeek with Culture\\_5 ($d = 0.581$) achieves comparable Novelty performance to Claude Opus at 60× lower cost (\\$0.42 vs. \\$25.00 per 1M output tokens). GPT with Culture\\_5 ($d = 0.501$) achieves similar performance at 36× lower cost (\\$2.00 vs. \\$25.00).""",
    """Beyond within-family comparisons, small models with personas can outperform larger models from competing providers. DeepSeek with Culture\\_5 ($d = 0.664$) achieves comparable Novelty performance to Claude Opus at 60× lower cost (\\$0.42 vs. \\$25.00 per 1M output tokens). GPT with Culture\\_5 ($d = 0.570$) achieves similar performance at 12.5× lower cost (\\$2.00 vs. \\$25.00).""")

rep("""Table~\\ref{tab:egr_complete} presents the complete EGR results for all model-persona combinations that achieved positive performance gains.""",
    """Table~\\ref{tab:egr_complete} presents the complete EGR results for all model-persona combinations with statistically significant positive performance gains.""")

rep("""GPT & Culture\\_5 & 0.501 & 87\\% & 9.17 \\\\
GPT & Culture\\_Expert & 0.301 & 87\\% & 8.53 \\\\
GPT & Culture\\_11 & 0.202 & 87\\% & 8.18 \\\\
Claude & Culture\\_5 & 0.908 & 40\\% & 2.25 \\\\
Claude & Culture\\_Expert & 0.252 & 40\\% & 1.85 \\\\
Claude & Culture\\_11 & 0.052 & 40\\% & 1.70 \\\\
DeepSeek & Culture\\_5 & 0.581 & 0\\% & 1.27 \\\\
DeepSeek & Culture\\_Expert & 0.402 & 0\\% & 1.19 \\\\
DeepSeek & Culture\\_11 & 0.003 & 0\\% & 1.00 \\\\""",
    """GPT & Culture\\_5 & 0.570 & 87\\% & 9.15 \\\\
GPT & Culture\\_Expert & 0.344 & 87\\% & 8.53 \\\\
Claude & Culture\\_5 & 1.087 & 40\\% & 2.24 \\\\
Claude & Culture\\_Expert & 0.281 & 40\\% & 1.84 \\\\
DeepSeek & Culture\\_5 & 0.664 & 0\\% & 1.27 \\\\
DeepSeek & Culture\\_Expert & 0.464 & 0\\% & 1.19 \\\\""")

rep("""\\textbf{GPT combinations} achieve exceptional economic value across all personas (EGR = 8.18-9.17), delivering 87\\% cost savings with positive performance gains.

\\textbf{Claude with Culture\\_5} achieves strong economic value (EGR = 2.25), delivering 40\\% cost savings with a large performance gain ($d = 0.908$).

\\textbf{DeepSeek combinations} achieve modest economic value (EGR = 1.00-1.27), with cost parity (0\\% savings) but positive performance gains.""",
    """\\textbf{GPT combinations} achieve exceptional economic value for Culture\\_5 and Culture\\_Expert (EGR = 8.53-9.15), delivering 87\\% cost savings with significant positive performance gains.

\\textbf{Claude with Culture\\_5} achieves strong economic value (EGR = 2.24), delivering 40\\% cost savings with a large performance gain ($d = 1.087$).

\\textbf{DeepSeek combinations} achieve modest economic value (EGR = 1.19-1.27), with cost parity (0\\% savings) but significant positive performance gains.""")

rep("""Small models with personas can achieve superior Novelty performance at 40-87\\% lower cost. The EGR provides a unified metric for comparing economic efficiency across model families, with GPT achieving exceptional value and Claude achieving strong value (See Figure~\\ref{fig:egr_bar_novelty}).""",
    """For the six significant combinations, small models with personas achieve superior Novelty performance at 40-87\\% lower cost. The EGR provides a unified metric for comparing economic efficiency across model families, with GPT achieving exceptional value and Claude achieving strong value (See Figure~\\ref{fig:egr_bar_novelty}).""")

# ============ 4.5 Robustness ============
rep("""Post-hoc power analysis showed mean power of 0.771, with 71.4\\% of comparisons achieving sufficient power ($\\ge 0.80$).""",
    """Post-hoc power analysis at the response level showed mean power of 0.544, with 38.1\\% of comparisons achieving sufficient power ($\\ge 0.80$). Most comparisons are therefore underpowered at the correct unit of analysis: non-significant results should be read as insufficient evidence rather than as evidence of no effect, and the corrected confidence intervals (Table~\\ref{tab:effects_complete}) widen accordingly.""")

rep("""Leave-one-out sensitivity analysis confirmed that results are highly stable, with 100\\% of effects showing changes below the stability threshold of $|\\Delta| < 0.1$ when removing any single model. The mean absolute change across all comparisons was $0.039$, with a maximum change of $0.098$ (observed when removing Qwen for Culture\\_5). Qwen had the largest average impact ($|\\Delta| = 0.069$), followed by Claude ($|\\Delta| = 0.054$), while Llama had the smallest impact ($|\\Delta| = 0.016$). These findings indicate that while some models exert greater influence on the average effect sizes than others, no single model drives the observed patterns.""",
    """Leave-one-out sensitivity analysis confirmed that results are highly stable, with 19 of 21 effects (90\\%) showing changes below the stability threshold of $|\\Delta| < 0.1$ when removing any single model. The mean absolute change across all comparisons was $0.047$, with a maximum change of $0.117$ (observed when removing Claude for Culture\\_5). Qwen had the largest average impact ($|\\Delta| = 0.083$), followed by Claude ($|\\Delta| = 0.065$), while Llama had the smallest impact ($|\\Delta| = 0.018$). These findings indicate that while some models exert greater influence on the average effect sizes than others, no single model drives the observed patterns.""")

rep("""Isolation Forest analysis (contamination = 0.1) identified 5.1\\% of responses as outliers. Removing outliers did not meaningfully change effect sizes ($\\Delta < 0.04$).""",
    """Isolation Forest analysis (contamination = 0.1) flagged 10.0\\% of responses as outliers (the contamination parameter fixes the flagged share). Removing them changed pooled persona effect sizes by at most $\\Delta = 0.03$.""")

rep("""Train-test split (80/20 by problem) confirmed that findings generalize to new problems:
- Culture\\_5: train $d = 0.305$, test $d = 0.274$ ($\\Delta = 0.031$)
- Culture\\_Expert: train $d = 0.099$, test $d = 0.119$ ($\\Delta = -0.020$)
- Culture\\_11: train $d = -0.149$, test $d = -0.138$ ($\\Delta = -0.011$)

All differences $|\\Delta| < 0.2$, confirming generalizability.""",
    """Train-test split (80/20 by problem, stratified by domain) confirmed that the direction of persona effects generalizes to new problems:
- Culture\\_5: train $d = 0.307$, test $d = 0.544$ ($\\Delta = +0.237$)
- Culture\\_Expert: train $d = 0.086$, test $d = 0.281$ ($\\Delta = +0.195$)
- Culture\\_11: train $d = -0.183$, test $d = -0.113$ ($\\Delta = +0.070$)

Signs are consistent across splits for all three personas; magnitudes vary more at the response level (maximum $|\\Delta| = 0.24$) because the test split contains only about 20 responses per condition.""")

rep("""Our findings are reliable, not driven by outliers, and generalize to new problems. The leave-one-out sensitivity analysis confirms that while some models (particularly Qwen and Claude) exert greater influence on average effect sizes than others, no single model drives the observed patterns (all changes $|\\Delta| < 0.1$).""",
    """Our findings are reliable, not driven by outliers, and generalize in direction to new problems. The leave-one-out sensitivity analysis confirms that while some models (particularly Qwen and Claude) exert greater influence on average effect sizes than others, no single model drives the observed patterns (19/21 changes $|\\Delta| < 0.1$, maximum 0.117).""")

# ============ 4.6 Table 9 ============
rep("""\\textbf{1. Model-Dependent} & Persona effects on Novelty vary dramatically across models. Claude with Culture\\_5 shows a large positive effect ($d = 0.908$); Qwen with Culture\\_11 shows a medium negative effect ($d = -0.519$). \\\\
\\midrule
\\textbf{2. Regional Moderation (Weak)} & Eastern models show marginally greater responsiveness to Culture\\_Expert, but evidence is inconclusive (Bayes Factor $= 0.331$). \\\\
\\midrule
\\textbf{3. Domain Specificity} & Culture\\_5 performs best on General Knowledge ($d = 0.495$) and Reasoning ($d = 0.453$); Culture\\_11 consistently harms Novelty across all domains. \\\\
\\midrule
\\textbf{4. Economic Advantage} & Small models with personas achieve 40-87\\% cost savings. GPT achieves exceptional economic value (EGR up to 9.17); Claude achieves strong value (EGR $= 2.25$). \\\\
\\midrule
\\textbf{5. Robustness} & Results are stable (mean absolute change $= 0.039$, all changes $|\\Delta| < 0.1$), generalize to new problems ($|\\Delta| < 0.2$), and are not driven by outliers. \\\\""",
    """\\textbf{1. Model-Dependent} & Persona effects on Novelty vary dramatically across models. Claude with Culture\\_5 shows a large positive effect ($d = 1.087$); Qwen with Culture\\_11 shows a medium negative effect ($d = -0.638$). \\\\
\\midrule
\\textbf{2. No Regional Moderation} & Training region did not moderate persona effects at the response level (interaction $p = 0.445$; Bayes Factor $= 0.331$). \\\\
\\midrule
\\textbf{3. Domain Specificity} & Culture\\_5 performs best on General Knowledge ($d = 0.628$) and Reasoning ($d = 0.545$); Culture\\_11 harms Novelty across all domains. \\\\
\\midrule
\\textbf{4. Economic Advantage} & Six significant small-model + persona combinations achieve 40-87\\% cost savings. GPT achieves exceptional economic value (EGR up to 9.15); Claude achieves strong value (EGR $= 2.24$). \\\\
\\midrule
\\textbf{5. Robustness} & Results are stable (mean absolute change $= 0.047$, 19/21 changes $|\\Delta| < 0.1$), generalize in direction to new problems, and are not driven by outliers. \\\\""")

# ============ 4.7 Gemini ============
rep("""    \\item **Judge confusion**: The presence of extensive reasoning traces may have confused judge models, which were expecting only the final answer based on the response format of other models.
    \\item **Task mismatch**: For structured extraction tasks (Problems 3-5), Gemini's output format deviated from the requested JSON schema, likely resulting in lower scores regardless of content quality.""",
    """    \\item \\textbf{Judge confusion}: The presence of extensive reasoning traces may have confused judge models, which were expecting only the final answer based on the response format of other models.
    \\item \\textbf{Task mismatch}: For structured extraction tasks (Problems 3-5), Gemini's output format deviated from the requested JSON schema, likely resulting in lower scores regardless of content quality.""")

rep("""These factors explain Gemini's anomalously low baseline Novelty scores ($M = 1.39$ vs. $2.69$ average for other models) and its negligible persona effects (all $|d| < 0.3$). Direct comparisons between Gemini and other models should be interpreted with caution, as the format inconsistency represents a measurement artifact rather than a genuine difference in model capability.""",
    """These factors explain Gemini's anomalously low Novelty scores ($M = 1.39$ vs. $2.70$ across all conditions for the other models; $M = 1.41$ vs. $2.60$ on the unsteered large baseline) and its largely negligible persona effects (Culture\\_5 and Culture\\_Expert $|d| < 0.14$, non-significant; Culture\\_11 $d = -0.443$). Direct comparisons between Gemini and other models should be interpreted with caution, as the format inconsistency represents a measurement artifact rather than a genuine difference in model capability. Accordingly, Gemini is excluded from the economic analysis (Section 3.7.3) and from the domain-level robustness check (Section 4.3); pooled results include Gemini unless stated otherwise.""")

# ============ 5 Discussion ============
rep("""This study evaluated whether small LLMs steered with cultural personas could outperform large LLMs on Novelty. Through a systematic evaluation of seven models across 100 problems, we find that persona effectiveness follows a contingency model rather than a universal rule. Novelty was the only dimension with good inter-rater reliability (\\(\\kappa = 0.68\\)), justifying our focused analysis.""",
    """This study evaluated whether small LLMs steered with cultural personas could outperform large LLMs on Novelty. Through a systematic evaluation of seven models across 100 problems, we find that persona effectiveness follows a contingency model rather than a universal rule. Inter-rater reliability was fair-to-moderate and statistically indistinguishable across the four core creativity dimensions (\\(\\kappa = 0.31\\)--\\(0.33\\)); we focus on Novelty as the construct central to our research question.""")

rep("""Persona effects on Novelty vary dramatically across architectures. Claude with Culture\\_5 showed a large positive effect (\\(d = 0.908\\)), while Qwen with Culture\\_11 showed a medium negative effect (\\(d = -0.519\\)). This aligns with PersonaGym benchmark findings that persona capability is a distinct dimension of intelligence that does not scale linearly with model size (\\cite{samuel2024personagym}). The dissociation where smaller models (DeepSeek, 7B parameters) outperform larger models (Mistral, 24B) in persona effectiveness confirms that raw parameter count is not a reliable predictor of persona faithfulness.""",
    """Persona effects on Novelty vary dramatically across architectures. Claude with Culture\\_5 showed a large positive effect (\\(d = 1.087\\)), while Qwen with Culture\\_11 showed a medium negative effect (\\(d = -0.638\\)). This aligns with PersonaGym benchmark findings that persona capability is a distinct dimension of intelligence that does not scale linearly with model size (\\cite{vinay_samuel_301ec4c0}). The dissociation whereby the far cheaper DeepSeek pair shows substantially larger persona effects than the Mistral pair confirms that neither cost nor raw parameter count is a reliable predictor of persona faithfulness.""")

rep("""The finding that DeepSeek, a smaller MoE model, achieves a medium positive effect with Culture\\_5 (\\(d = 0.581\\)) suggests that MoE architectures may be particularly well-suited for persona-based steering on Novelty.""",
    """The finding that DeepSeek, an MoE model far cheaper than its Western peers, achieves a medium positive effect with Culture\\_5 (\\(d = 0.664\\)) suggests that MoE architectures may be particularly well-suited for persona-based steering on Novelty.""")

rep("""We found weak evidence for regional moderation. While the moderation analysis showed a statistically significant interaction (\\(t = 2.08\\), \\(p = 0.037\\)), the Bayes Factor (\\(BF = 0.331\\)) provided anecdotal evidence against the moderation hypothesis. This discrepancy highlights the limitations of relying solely on frequentist significance thresholds, especially with unbalanced sample sizes (2 Eastern vs. 5 Western models). The marginal ANOVA interaction (\\(p = 0.052\\)) further supports the interpretation that regional differences, if present, are small.

Quantitatively, Eastern models showed slightly stronger positive effects from Culture\\_Expert (\\(d = +0.144\\)) compared to Western models (\\(d = +0.023\\)), but the evidence is inconclusive. The persistence of Western-default bias even in Eastern models (\\cite{bolei_ma_78d40201}) suggests that pluralistic alignment—where models can dynamically shift cultural dimensions based on context—remains an unsolved challenge (\\cite{kharchenkoHowWellLLMs2024}).""",
    """We found no evidence for regional moderation at the response level: the persona \\(\\times\\) region interaction was non-significant in both the ANOVA (\\(F(3, 2810) = 0.89\\), \\(p = 0.445\\)) and the moderation regression (\\(t = -1.27\\), \\(p = 0.21\\)), in agreement with the Bayes Factor (\\(BF = 0.331\\)), which provides anecdotal evidence against the moderation hypothesis. The frequentist significance reported in earlier analyses was an artifact of treating nine judge ratings per response as independent observations---an instructive case where the Bayesian evidence pointed to the correct conclusion from the start.

Descriptively, Western models showed slightly larger mean effects for the positive personas (Culture\\_Expert: \\(d = +0.140\\) Western vs. \\(d = +0.050\\) Eastern), contrary to the rating-level pattern; none of these differences approaches significance. The persistence of Western-default bias even in Eastern models (\\cite{bolei_ma_78d40201}) suggests that pluralistic alignment—where models can dynamically shift cultural dimensions based on context—remains an unsolved challenge (\\cite{kharchenkoHowWellLLMs2024}).""")

rep("""Culture\\_5 performed best on General Knowledge problems (\\(d = 0.495\\)) and Reasoning problems (\\(d = 0.453\\)), with smaller effects on Creative (\\(d = 0.207\\)) and Instruction (\\(d = 0.159\\)).""",
    """Culture\\_5 performed best on General Knowledge problems (\\(d = 0.628\\)) and Reasoning problems (\\(d = 0.545\\)), with smaller effects on Creative (\\(d = 0.233\\)) and Instruction (\\(d = 0.185\\)).""")

rep("""Notably, Culture\\_11 consistently harmed Novelty across all domains, with the most negative effects on Instruction (\\(d = -0.198\\)) and Creative (\\(d = -0.170\\)).""",
    """Notably, Culture\\_11 harmed Novelty across all domains, with the most negative effects on Instruction (\\(d = -0.229\\)) and Creative (\\(d = -0.196\\)).""")

rep("""Our inter-rater reliability analysis revealed that Novelty was the only dimension with good agreement among judges (\\(\\kappa = 0.68\\)). Other dimensions—particularly Usefulness (\\(\\kappa = 0.15\\)) and Cultural Sensitivity (\\(\\kappa = -0.23\\))—exhibited poor to fair reliability. This finding has important methodological implications: subjective dimensions like Usefulness and Cultural Sensitivity may be more difficult for LLM judges to assess consistently, suggesting that future work should focus on more objective criteria or incorporate human raters for validation.""",
    """Our inter-rater reliability analysis found fair-to-moderate agreement for the four core dimensions (\\(\\kappa = 0.31\\)--\\(0.33\\)) and poor agreement for Cultural Sensitivity (\\(\\kappa = 0.17\\)). Notably, the core dimensions are statistically indistinguishable in reliability, so our focus on Novelty rests on its centrality to the research question rather than on superior measurement. This finding has important methodological implications: subjective dimensions like Cultural Sensitivity may be more difficult for LLM judges to assess consistently, suggesting that future work should focus on more objective criteria or incorporate human raters for validation.""")

# ============ 5.2 Practical ============
rep("""    \\item \\textbf{Use Claude with Culture\\_5} for the largest Novelty gains (\\(d = 0.908\\)) when cost is not the primary concern (40\\% cost savings).
    \\item \\textbf{Use GPT with Culture\\_5} for the best balance of Novelty improvement (\\(d = 0.501\\)) and cost savings (87\\%).
    \\item \\textbf{Avoid Culture\\_11} for Novelty across all models and domains, as it consistently harms performance.
    \\item \\textbf{For General Knowledge and Reasoning tasks}, Culture\\_5 is particularly effective.""",
    """    \\item \\textbf{Use Claude with Culture\\_5} for the largest Novelty gains (\\(d = 1.087\\)) when cost is not the primary concern (40\\% cost savings).
    \\item \\textbf{Use GPT with Culture\\_5} for the best balance of Novelty improvement (\\(d = 0.570\\)) and cost savings (87\\%).
    \\item \\textbf{Avoid Culture\\_11} for Qwen, Mistral, Llama, and Gemini, where it significantly harms Novelty; it shows no significant benefit for any model.
    \\item \\textbf{For General Knowledge and Reasoning tasks}, Culture\\_5 is particularly effective.""")

rep("""Eastern-trained models (DeepSeek, Qwen) showed mixed results. DeepSeek benefited substantially from Culture\\_5 (\\(d = 0.581\\)), while Qwen was harmed by all personas (negative effects ranging from \\(-0.185\\) to \\(-0.519\\)). This suggests that Eastern origin alone does not guarantee persona effectiveness; architectural factors may be more important.

Western models showed divergent patterns: Claude benefited strongly (\\(d = 0.908\\)), GPT showed moderate benefits (\\(d = 0.202-0.501\\)), while Llama and Mistral showed mixed or negative effects. Gemini showed negligible effects across all personas (\\(|d| < 0.3\\)), with unusually low baseline Novelty scores (1.41 vs. 2.64 average for other models).""",
    """Eastern-trained models (DeepSeek, Qwen) showed mixed results. DeepSeek benefited substantially from Culture\\_5 (\\(d = 0.664\\)), while Qwen was harmed by all personas (negative effects ranging from \\(-0.229\\) to \\(-0.638\\), significant for Culture\\_Expert and Culture\\_11). This suggests that Eastern origin alone does not guarantee persona effectiveness; architectural factors may be more important.

Western models showed divergent patterns: Claude benefited strongly (\\(d = 1.087\\)), GPT showed moderate benefits (\\(d = 0.231-0.570\\)), while Llama and Mistral showed mixed or negative effects. Gemini showed negligible, non-significant effects for Culture\\_5 and Culture\\_Expert and a significant negative Culture\\_11 effect (\\(d = -0.443\\)), with unusually low baseline Novelty scores (1.41 vs. 2.60 average for other models) that Section 4.7 attributes in part to a measurement artifact.""")

rep("""    \\item \\textbf{GPT combinations} achieve exceptional economic value (EGR = 8.18-9.17), making them the best choice for cost-sensitive applications.
    \\item \\textbf{Claude with Culture\\_5} achieves strong economic value (EGR = 2.25), making it the best choice for applications where maximizing Novelty is the primary goal.
    \\item \\textbf{DeepSeek with Culture\\_5} achieves modest economic value (EGR = 1.27) with no cost savings but positive performance gains, suitable when model cost is not a constraint.""",
    """    \\item \\textbf{GPT combinations} achieve exceptional economic value (EGR = 8.53-9.15), making them the best choice for cost-sensitive applications.
    \\item \\textbf{Claude with Culture\\_5} achieves strong economic value (EGR = 2.24), making it the best choice for applications where maximizing Novelty is the primary goal.
    \\item \\textbf{DeepSeek with Culture\\_5} achieves modest economic value (EGR = 1.27) with no cost savings but significant positive performance gains, suitable when model cost is not a constraint.""")

rep("""Maximize Novelty & Claude + Culture\\_5 & 0.908 & 40\\% & 2.25 \\\\
Maximize Cost-Efficiency & GPT + Culture\\_5 & 0.501 & 87\\% & 9.17 \\\\
Balanced Trade-off & GPT + Culture\\_Expert & 0.301 & 87\\% & 8.53 \\\\
\\midrule
\\textbf{Avoid at all costs} & \\textbf{Any model + Culture\\_11} & \\textbf{-0.519 to -0.118} & \\textbf{---} & \\textbf{---} \\\\
\\bottomrule
\\end{tabular}
\\caption*{\\footnotesize For Novelty outcomes. Culture\\_11 consistently harms performance across all models and domains. EGR = Efficiency Gain Ratio.}""",
    """Maximize Novelty & Claude + Culture\\_5 & 1.087 & 40\\% & 2.24 \\\\
Maximize Cost-Efficiency & GPT + Culture\\_5 & 0.570 & 87\\% & 9.15 \\\\
Balanced Trade-off & GPT + Culture\\_Expert & 0.344 & 87\\% & 8.53 \\\\
\\midrule
\\textbf{Avoid} & \\textbf{Qwen, Mistral, Llama, Gemini + Culture\\_11} & \\textbf{-0.638 to -0.412} & \\textbf{---} & \\textbf{---} \\\\
\\bottomrule
\\end{tabular}
\\caption*{\\footnotesize For Novelty outcomes. Culture\\_11 significantly harms Novelty for Qwen, Mistral, Llama, and Gemini (\\(d = -0.638\\) to \\(-0.412\\)) and shows no significant benefit for any model. EGR = Efficiency Gain Ratio.}""")

# ============ 5.3 Limitations ============
rep("""Fourth, inter-rater reliability varied across dimensions. While Novelty showed good agreement (\\(\\kappa = 0.68\\)), other dimensions—particularly Usefulness (\\(\\kappa = 0.15\\)) and Cultural Sensitivity (\\(\\kappa = -0.23\\))—exhibited poor reliability. This suggests that these constructs may be more subjective or context-dependent, and findings related to them should be interpreted with caution. Consequently, we focused our primary analysis on Novelty.

Fifth, the Bayes Factor for regional moderation (\\(BF = 0.331\\)) indicates weak evidence, and our sample of Eastern models was small (2 models vs. 5 Western models). Future research with more Eastern models is needed to draw definitive conclusions.

Sixth, as detailed in Section 4.6, Gemini's unique response format (with reasoning traces not present in other models) represents a measurement artifact that limits direct comparability.""",
    """Fourth, inter-rater reliability was only fair-to-moderate for the four core dimensions (\\(\\kappa = 0.31\\)--\\(0.33\\)) and poor for Cultural Sensitivity (\\(\\kappa = 0.17\\)). The non-primary dimensions should be treated as exploratory, and even the Novelty conclusions would benefit from validation with human raters.

Fifth, although no regional moderation was detected (interaction \\(p = 0.445\\); \\(BF = 0.331\\)), our sample of Eastern models was small (2 models vs. 5 Western models), limiting power to detect moderation. Future research with more Eastern models is needed to draw definitive conclusions.

Sixth, as detailed in Section 4.7, Gemini's unique response format (with reasoning traces not present in other models) represents a measurement artifact that limits direct comparability.""")

rep("""Seventh, while our leave-one-out sensitivity analysis confirmed that results are stable, Qwen and Claude had a larger influence on average effect sizes than other models. This suggests that replication with a broader set of models would further strengthen the generalizability of our findings.""",
    """Seventh, while our leave-one-out sensitivity analysis confirmed that results are stable, Qwen and Claude had a larger influence on average effect sizes than other models. This suggests that replication with a broader set of models would further strengthen the generalizability of our findings.

Eighth, post-hoc power was limited at the response level (mean power 0.544; 38.1\\% of comparisons \\(\\ge 0.80\\)), so null results are inconclusive rather than evidence of absence. In addition, GPT Culture\\_5 includes 120 responses across the 100 problems (20 problems were generated twice); sensitivity checks averaging duplicates per problem leave the conclusion unchanged (\\(d = 0.624\\) vs. \\(0.570\\)).""")

rep("""Third, the poor inter-rater reliability for Usefulness and Cultural Sensitivity suggests that future work should explore alternative evaluation methods, potentially incorporating human raters or refined rubrics.""",
    """Third, the limited inter-rater reliability for the non-primary dimensions (particularly Cultural Sensitivity) suggests that future work should explore alternative evaluation methods, potentially incorporating human raters or refined rubrics.""")

# ============ Appendix A.1 ============
rep("""\\caption{Mean vs. median Novelty scores. The high correlation ($r = 0.997$) indicates that results are robust against outliers.}""",
    """\\caption{Mean vs. median Novelty scores (response level, 28 model $\\times$ condition cells). The high correlation ($r = 0.983$) indicates that results are robust against outliers.}""")

rep("""The correlation between mean and median Novelty scores is $r = 0.997$ ($p < 0.001$), confirming that our findings are not artifacts of extreme outliers. The mean-median differences range from $-0.031$ to $+0.028$, well within acceptable bounds for robustness.""",
    """The correlation between mean and median Novelty scores is $r = 0.983$ ($p < 0.001$), confirming that our findings are not artifacts of extreme outliers. Mean-median differences at the response level range from $-0.33$ to $+0.36$ across the 28 cells, reflecting the coarser scale of response-level averages; the near-unity correlation confirms that the rank ordering of cells is preserved.""")

# ============ Appendix A.2 (Table 11: descriptives, response grain) ============
rep(r"""Table~\ref{tab:desc_novelty_full} presents the complete descriptive statistics for Novelty across all models and conditions, including standard deviations and sample sizes.""",
    r"""Table~\ref{tab:desc_novelty_full} presents the complete response-level descriptive statistics for Novelty across all models and conditions (n = number of responses; each response is the mean of nine judge ratings). GPT Culture\_5 includes 120 responses across the 100 problems (20 problems were generated twice).""")

rep(r"""\multirow{4}{*}{Claude} & Culture\_5 & 3.81 & 0.88 & 893 \\
 & Culture\_Expert & 3.14 & 1.22 & 890 \\
 & Culture\_11 & 2.89 & 1.12 & 893 \\
 & Large Baseline & 2.82 & 1.26 & 893 \\""",
    r"""\multirow{4}{*}{Claude} & Culture\_5 & 3.81 & 0.64 & 100 \\
 & Culture\_Expert & 3.14 & 1.06 & 100 \\
 & Culture\_11 & 2.89 & 0.95 & 100 \\
 & Large Baseline & 2.84 & 1.09 & 100 \\""")

rep(r"""\multirow{4}{*}{DeepSeek} & Culture\_5 & 3.35 & 1.15 & 893 \\
 & Culture\_Expert & 3.13 & 1.18 & 893 \\
 & Culture\_11 & 2.64 & 1.16 & 896 \\
 & Large Baseline & 2.64 & 1.28 & 884 \\""",
    r"""\multirow{4}{*}{DeepSeek} & Culture\_5 & 3.35 & 1.02 & 100 \\
 & Culture\_Expert & 3.14 & 1.03 & 100 \\
 & Culture\_11 & 2.64 & 1.00 & 100 \\
 & Large Baseline & 2.64 & 1.13 & 100 \\""")

rep(r"""\multirow{4}{*}{GPT} & Culture\_5 & 3.23 & 1.13 & 1063 \\
 & Culture\_Expert & 3.00 & 1.19 & 890 \\
 & Culture\_11 & 2.88 & 1.16 & 882 \\
 & Large Baseline & 2.64 & 1.22 & 889 \\""",
    r"""\multirow{4}{*}{GPT} & Culture\_5 & 3.22 & 0.99 & 120 \\
 & Culture\_Expert & 3.00 & 1.04 & 100 \\
 & Culture\_11 & 2.88 & 1.02 & 100 \\
 & Large Baseline & 2.64 & 1.06 & 100 \\""")

rep(r"""\multirow{4}{*}{Llama} & Culture\_5 & 2.50 & 1.03 & 900 \\
 & Culture\_Expert & 2.35 & 0.95 & 900 \\
 & Culture\_11 & 1.97 & 0.93 & 900 \\
 & Large Baseline & 2.29 & 1.06 & 900 \\""",
    r"""\multirow{4}{*}{Llama} & Culture\_5 & 2.50 & 0.74 & 100 \\
 & Culture\_Expert & 2.34 & 0.68 & 100 \\
 & Culture\_11 & 1.97 & 0.68 & 100 \\
 & Large Baseline & 2.29 & 0.86 & 100 \\""")

rep(r"""\multirow{4}{*}{Mistral} & Culture\_5 & 2.50 & 1.05 & 900 \\
 & Culture\_Expert & 2.30 & 0.99 & 900 \\
 & Culture\_11 & 1.95 & 0.99 & 900 \\
 & Large Baseline & 2.36 & 1.06 & 891 \\""",
    r"""\multirow{4}{*}{Mistral} & Culture\_5 & 2.50 & 0.74 & 100 \\
 & Culture\_Expert & 2.29 & 0.74 & 100 \\
 & Culture\_11 & 1.95 & 0.80 & 100 \\
 & Large Baseline & 2.36 & 0.85 & 99 \\""")

rep(r"""\multirow{4}{*}{Qwen} & Culture\_5 & 2.63 & 0.99 & 900 \\
 & Culture\_Expert & 2.51 & 0.94 & 900 \\
 & Culture\_11 & 2.26 & 0.99 & 899 \\
 & Large Baseline & 2.83 & 1.23 & 900 \\""",
    r"""\multirow{4}{*}{Qwen} & Culture\_5 & 2.63 & 0.71 & 100 \\
 & Culture\_Expert & 2.51 & 0.69 & 100 \\
 & Culture\_11 & 2.26 & 0.72 & 100 \\
 & Large Baseline & 2.83 & 1.05 & 100 \\""")

rep(r"""\multirow{4}{*}{Gemini} & Culture\_5 & 1.49 & 0.98 & 893 \\
 & Culture\_Expert & 1.45 & 0.86 & 888 \\
 & Culture\_11 & 1.21 & 0.55 & 888 \\
 & Large Baseline & 1.41 & 0.85 & 884 \\""",
    r"""\multirow{4}{*}{Gemini} & Culture\_5 & 1.49 & 0.73 & 100 \\
 & Culture\_Expert & 1.45 & 0.56 & 100 \\
 & Culture\_11 & 1.21 & 0.34 & 100 \\
 & Large Baseline & 1.41 & 0.55 & 99 \\""")

# ============ Appendix A.3 (Table 12: domain effects, response grain) ============
rep(r"""Culture\_5 & 0.207 & 0.495 & 0.159 & 0.453 \\
Culture\_Expert & 0.032 & 0.174 & 0.079 & 0.175 \\
Culture\_11 & -0.170 & -0.118 & -0.198 & -0.124 \\""",
    r"""Culture\_5 & 0.233 & 0.628 & 0.185 & 0.545 \\
Culture\_Expert & 0.036 & 0.223 & 0.092 & 0.210 \\
Culture\_11 & -0.196 & -0.154 & -0.229 & -0.149 \\""")

# ============ Appendix A.4 (Table 13: power, response grain) ============
rep(r"""Claude & 0.95 & 0.82 & 0.78 \\
DeepSeek & 0.92 & 0.98 & 0.76 \\
GPT & 0.88 & 0.91 & 0.85 \\
Llama & 0.85 & 0.72 & 0.99 \\
Mistral & 0.98 & 0.81 & 1.00 \\
Qwen & 0.94 & 0.79 & 0.99 \\
Gemini & 0.79 & 0.68 & 0.94 \\""",
    r"""Claude & 1.00 & 0.51 & 0.07 \\
DeepSeek & 1.00 & 0.90 & 0.05 \\
GPT & 0.99 & 0.68 & 0.37 \\
Llama & 0.48 & 0.08 & 0.83 \\
Mistral & 0.26 & 0.08 & 0.94 \\
Qwen & 0.36 & 0.73 & 0.99 \\
Gemini & 0.15 & 0.08 & 0.88 \\""")

rep(r"""Values $>0.80$ indicate sufficient power. Mean power = 0.771; 71.4\% of comparisons achieved sufficient power.""",
    r"""Values $>0.80$ indicate sufficient power. Response-level power (n $\approx$ 100 per cell): mean power = 0.544; 38.1\% of comparisons achieved sufficient power.""")

# ============ Appendix A.5 (Table 14: LOO, response grain) ============
rep(r"""Qwen & 0.069 \\
Claude & 0.054 \\
GPT & 0.042 \\
DeepSeek & 0.041 \\
Mistral & 0.031 \\
Gemini & 0.021 \\
Llama & 0.016 \\""",
    r"""Qwen & 0.083 \\
Claude & 0.065 \\
GPT & 0.050 \\
DeepSeek & 0.049 \\
Mistral & 0.036 \\
Gemini & 0.027 \\
Llama & 0.018 \\""")

rep(r"""Mean absolute change in Cohen's d when each model is removed. All changes $|\Delta| < 0.1$, indicating high stability. Qwen and Claude have the largest impact, while Llama has the smallest. No single model drives the observed patterns.""",
    r"""Mean absolute change in Cohen's d when each model is removed (response level, 21 effect sizes). 19 of 21 changes satisfy $|\Delta| < 0.1$; the largest is 0.117 (removing Claude, Culture\_5). Qwen and Claude have the largest impact, while Llama has the smallest. No single model drives the observed patterns.""")

# ============ Appendix A.7 (Table 16: other dimensions, response grain, all 7 models) ============
rep(r"""Table~\ref{tab:other_dimensions} presents the mean scores for Usefulness, Flexibility, Elaboration, and Cultural Sensitivity. These results are reported as exploratory due to poor inter-rater reliability (see Section 3.6).""",
    r"""Table~\ref{tab:other_dimensions} presents the response-level mean scores for Usefulness, Flexibility, Elaboration, and Cultural Sensitivity. These results are reported as exploratory due to limited inter-rater reliability (Section 3.6).""")

rep(r"""\multirow{4}{*}{Claude} & Culture\_5 & 4.38 & 4.31 & 4.15 & 4.12 \\
 & Culture\_Expert & 4.35 & 4.18 & 4.08 & 4.05 \\
 & Culture\_11 & 4.28 & 4.05 & 3.98 & 3.92 \\
 & Baseline & 4.20 & 4.02 & 3.95 & 3.88 \\
\midrule
\multirow{4}{*}{DeepSeek} & Culture\_5 & 4.28 & 4.22 & 4.05 & 3.98 \\
 & Culture\_Expert & 4.32 & 4.28 & 4.12 & 4.05 \\
 & Culture\_11 & 4.18 & 3.95 & 3.85 & 3.78 \\
 & Baseline & 4.05 & 3.88 & 3.75 & 3.68 \\
\midrule
\multirow{4}{*}{GPT} & Culture\_5 & 4.22 & 4.15 & 4.02 & 3.95 \\
 & Culture\_Expert & 4.25 & 4.18 & 4.05 & 3.98 \\
 & Culture\_11 & 4.18 & 4.08 & 3.95 & 3.88 \\
 & Baseline & 4.12 & 3.98 & 3.85 & 3.78 \\
\midrule
\multirow{4}{*}{Gemini} & Culture\_5 & 1.60 & 1.49 & 3.42 & 3.80 \\
 & Culture\_Expert & 1.55 & 1.45 & 3.35 & 3.75 \\
 & Culture\_11 & 1.48 & 1.38 & 3.28 & 3.65 \\
 & Baseline & 1.52 & 1.42 & 3.32 & 3.70 \\
\bottomrule
\end{tabular}
\caption*{\footnotesize These results should be interpreted with caution due to poor inter-rater reliability (Fleiss' $\kappa$: Usefulness $= 0.15$, Flexibility $= 0.30$, Elaboration $= 0.30$, Cultural Sensitivity $= -0.23$).}""",
    r"""\multirow{4}{*}{Claude} & Culture\_5 & 4.55 & 3.89 & 4.66 & 4.47 \\
 & Culture\_Expert & 4.75 & 3.69 & 4.74 & 4.42 \\
 & Culture\_11 & 4.63 & 3.50 & 4.68 & 4.42 \\
 & Large Baseline & 4.65 & 3.39 & 4.67 & 4.45 \\
\midrule
\multirow{4}{*}{DeepSeek} & Culture\_5 & 4.45 & 3.72 & 4.42 & 4.37 \\
 & Culture\_Expert & 4.70 & 3.67 & 4.83 & 4.42 \\
 & Culture\_11 & 4.47 & 3.30 & 4.45 & 4.31 \\
 & Large Baseline & 4.42 & 3.17 & 4.23 & 4.33 \\
\midrule
\multirow{4}{*}{GPT} & Culture\_5 & 4.71 & 3.63 & 4.41 & 4.49 \\
 & Culture\_Expert & 4.81 & 3.71 & 4.62 & 4.41 \\
 & Culture\_11 & 4.74 & 3.66 & 4.51 & 4.45 \\
 & Large Baseline & 4.71 & 3.27 & 4.50 & 4.55 \\
\midrule
\multirow{4}{*}{Llama} & Culture\_5 & 3.69 & 2.77 & 3.83 & 4.26 \\
 & Culture\_Expert & 4.16 & 2.96 & 4.20 & 4.29 \\
 & Culture\_11 & 3.71 & 2.50 & 3.82 & 3.46 \\
 & Large Baseline & 4.38 & 2.82 & 4.24 & 4.44 \\
\midrule
\multirow{4}{*}{Mistral} & Culture\_5 & 3.70 & 2.84 & 3.81 & 3.88 \\
 & Culture\_Expert & 4.15 & 2.85 & 4.14 & 4.35 \\
 & Culture\_11 & 3.40 & 2.37 & 3.62 & 3.46 \\
 & Large Baseline & 4.54 & 2.97 & 4.38 & 4.50 \\
\midrule
\multirow{4}{*}{Qwen} & Culture\_5 & 4.14 & 3.12 & 4.01 & 4.22 \\
 & Culture\_Expert & 4.42 & 3.19 & 4.38 & 4.47 \\
 & Culture\_11 & 4.30 & 2.82 & 4.15 & 3.65 \\
 & Large Baseline & 4.60 & 3.37 & 4.60 & 4.49 \\
\midrule
\multirow{4}{*}{Gemini} & Culture\_5 & 1.42 & 1.53 & 3.14 & 3.77 \\
 & Culture\_Expert & 1.82 & 1.62 & 3.89 & 3.79 \\
 & Culture\_11 & 1.32 & 1.25 & 3.01 & 3.66 \\
 & Large Baseline & 1.83 & 1.57 & 3.67 & 3.97 \\
\bottomrule
\end{tabular}
\caption*{\footnotesize These results should be interpreted with caution due to limited inter-rater reliability (Fleiss' $\kappa$: Usefulness $= 0.32$, Flexibility $= 0.32$, Elaboration $= 0.31$, Cultural Sensitivity $= 0.17$). Values are response-level means (n $\approx$ 100 per cell).}""")

# ============ Appendix A.8 (Table 17: pure persona effects, response grain) ============
rep(r"""All comparisons use Novelty scores (the only dimension with good inter-rater 
reliability, \(\kappa = 0.68\)). Statistical significance is determined using 
FDR-corrected \(p < 0.05\) (indicated by \(^*\)).""",
    r"""All comparisons use Novelty scores (the primary dimension; full-data inter-rater 
reliability is fair, \(\kappa = 0.33\)). Statistical significance is determined using 
FDR-corrected \(p < 0.05\) (indicated by \(^*\)).""")

rep(r"""Claude & Culture 5 & 2.81 & 3.81 & 0.922 \\
Claude & Culture Expert & 2.81 & 3.13 & 0.263 \\
Claude & Culture 11 & 2.81 & 2.88 & 0.062 \\
DeepSeek & Culture 5 & 2.90 & 3.34 & 0.379 \\
DeepSeek & Culture Expert & 2.90 & 3.13 & 0.194 \\
DeepSeek & Culture 11 & 2.90 & 2.64 & -0.221 \\
GPT & Culture 5 & 2.76 & 3.23 & 0.395 \\
GPT & Culture Expert & 2.76 & 3.00 & 0.199 \\
GPT & Culture 11 & 2.76 & 2.88 & 0.099 \\
Llama & Culture 5 & 2.22 & 2.50 & 0.279$^*$ \\
Llama & Culture Expert & 2.22 & 2.34 & 0.125$^*$ \\
Llama & Culture 11 & 2.22 & 1.97 & -0.272$^*$ \\
Qwen & Culture 5 & 2.35 & 2.63 & 0.281$^*$ \\
Qwen & Culture Expert & 2.35 & 2.51 & 0.165$^*$ \\
Qwen & Culture 11 & 2.35 & 2.26 & -0.091 \\
Mistral & Culture 5 & 2.24 & 2.50 & 0.255$^*$ \\
Mistral & Culture Expert & 2.24 & 2.29 & 0.057 \\
Mistral & Culture 11 & 2.24 & 1.95 & -0.286$^*$ \\
Gemini & Culture 5 & 1.41 & 1.49 & 0.092 \\
Gemini & Culture Expert & 1.41 & 1.45 & 0.051 \\
Gemini & Culture 11 & 1.41 & 1.21 & -0.277 \\""",
    r"""Claude & Culture 5 & 2.82 & 3.81 & 1.101$^*$ \\
Claude & Culture Expert & 2.82 & 3.14 & 0.296 \\
Claude & Culture 11 & 2.82 & 2.89 & 0.073 \\
DeepSeek & Culture 5 & 2.91 & 3.35 & 0.432$^*$ \\
DeepSeek & Culture Expert & 2.91 & 3.14 & 0.224 \\
DeepSeek & Culture 11 & 2.91 & 2.64 & -0.258 \\
GPT & Culture 5 & 2.76 & 3.22 & 0.448$^*$ \\
GPT & Culture Expert & 2.76 & 3.00 & 0.228 \\
GPT & Culture 11 & 2.76 & 2.88 & 0.115 \\
Llama & Culture 5 & 2.22 & 2.50 & 0.386$^*$ \\
Llama & Culture Expert & 2.22 & 2.34 & 0.173 \\
Llama & Culture 11 & 2.22 & 1.97 & -0.374$^*$ \\
Qwen & Culture 5 & 2.35 & 2.63 & 0.379$^*$ \\
Qwen & Culture Expert & 2.35 & 2.51 & 0.221 \\
Qwen & Culture 11 & 2.35 & 2.26 & -0.120 \\
Mistral & Culture 5 & 2.24 & 2.50 & 0.345$^*$ \\
Mistral & Culture Expert & 2.24 & 2.29 & 0.075 \\
Mistral & Culture 11 & 2.24 & 1.95 & -0.363$^*$ \\
Gemini & Culture 5 & 1.41 & 1.49 & 0.130 \\
Gemini & Culture Expert & 1.41 & 1.45 & 0.077 \\
Gemini & Culture 11 & 1.41 & 1.21 & -0.396$^*$ \\""")

rep(r"""The pure persona effects are consistent with our main findings: 
Culture\_5 consistently improves Novelty across most models (largest effect: 
Claude, \(d = 0.922\)), while Culture\_11 shows negative or negligible effects 
for all models except Claude. The larger effect sizes observed here (compared to 
our main analysis) reflect the weaker baseline (small model without persona) 
rather than any inconsistency with our primary conclusions.""",
    r"""The pure persona effects are consistent with our main findings: 
Culture\_5 improves Novelty significantly for five of seven models (largest 
effect: Claude, \(d = 1.101\)), while Culture\_11 shows negative or negligible 
effects for all models. Note that the pure effects are not uniformly larger than 
the main-analysis contrasts: DeepSeek and GPT small baselines outscore their own 
large baselines, so their pure effects (0.432, 0.448) are smaller than the 
large-baseline contrasts (0.664, 0.570).""")

# ============ Figure paths (response-grain regenerated figures) ============
rep(r"{figure1_performance_barplot_novelty.png}", r"{figures_v2/figure1_performance_barplot_novelty.png}")
rep(r"{figure2_forest_plot_novelty.png}", r"{figures_v2/figure2_forest_plot_novelty.png}")
rep(r"{figure3_domain_heatmap_novelty.png}", r"{figures_v2/figure3_domain_heatmap_novelty.png}")
rep(r"{figure4_mds_plot_novelty.png}", r"{figures_v2/figure4_mds_plot_novelty.png}")
rep(r"{figure5_egr_bar_chart_novelty.png}", r"{figures_v2/figure5_egr_bar_chart_novelty.png}")
rep(r"{figure6_cost_performance_frontier_novelty.png}", r"{figures_v2/figure6_cost_performance_frontier_novelty.png}")
rep(r"{appendix_mean_vs_median_novelty.png}", r"{figures_v2/appendix_mean_vs_median_novelty.png}")

# ============ ROUND 2: fixes from the re-audit of the corrected draft ============
# 2.1 Llama/Mistral pooled means (verified against response_level.csv: 2.2647 / 2.2672)
rep(r"approximately 0.9 points below the next-lowest models (Llama and Mistral, both $M = 2.28$)",
    r"approximately 0.9 points below the next-lowest models (Llama, $M = 2.26$; Mistral, $M = 2.27$)")

# 2.2 Non-Gemini pooled mean (verified: mean of the six other pooled means = 2.666)
rep(r"($M = 1.39$ vs. $2.70$ across all conditions for the other models; $M = 1.41$ vs. $2.60$ on the unsteered large baseline)",
    r"($M = 1.39$ vs. $2.67$ across all conditions for the other models; $M = 1.41$ vs. $2.60$ on the unsteered large baseline)")

# 2.3 Train-test split: values must match frozen recompute/train_test_response.csv;
#     the split is a seeded random shuffle, NOT stratified by domain
rep(r"""Train-test split (80/20 by problem, stratified by domain) confirmed that the direction of persona effects generalizes to new problems:
- Culture\_5: train $d = 0.307$, test $d = 0.544$ ($\Delta = +0.237$)
- Culture\_Expert: train $d = 0.086$, test $d = 0.281$ ($\Delta = +0.195$)
- Culture\_11: train $d = -0.183$, test $d = -0.113$ ($\Delta = +0.070$)

Signs are consistent across splits for all three personas; magnitudes vary more at the response level (maximum $|\Delta| = 0.24$) because the test split contains only about 20 responses per condition.""",
    r"""Train-test split (random 80/20 split by problem, seed 42) confirmed that the direction of persona effects generalizes to new problems:
- Culture\_5: train $d = 0.310$, test $d = 0.515$ ($\Delta = +0.205$)
- Culture\_Expert: train $d = 0.085$, test $d = 0.271$ ($\Delta = +0.186$)
- Culture\_11: train $d = -0.186$, test $d = -0.097$ ($\Delta = +0.089$)

Signs are consistent across splits for all three personas; magnitudes vary more at the response level (maximum $|\Delta| = 0.21$) because the test split contains only about 20 responses per condition.""")

# 2.4 "40-87% lower cost" was false for DeepSeek (0% savings, cost parity) - 5 spots
rep(r"Economically, six model-persona combinations achieved significant performance gains at 40-87\% lower cost.",
    r"Economically, six model-persona combinations achieved significant performance gains at equal or lower cost than their large baselines (40-87\% savings for GPT and Claude; cost parity for DeepSeek).")
rep(r"demonstrating that small models with personas achieve significant performance gains at 40-87\% lower cost, with GPT combinations achieving exceptional economic value (EGR up to 9.15).",
    r"demonstrating that small models with personas achieve significant performance gains at equal or lower cost than their large baselines (40-87\% savings for GPT and Claude; cost parity for DeepSeek), with GPT combinations achieving exceptional economic value (EGR up to 9.15).")
rep(r"For the six significant combinations, small models with personas achieve superior Novelty performance at 40-87\% lower cost.",
    r"For the six significant combinations, small models with personas achieve superior Novelty performance at equal or lower cost (40-87\% savings for GPT and Claude; cost parity for DeepSeek).")
rep(r"Six significant small-model + persona combinations achieve 40-87\% cost savings.",
    r"Six small-model + persona combinations achieve significant gains at equal or lower cost (40-87\% savings for GPT and Claude; parity for DeepSeek).")
rep(r"Small models with personas can achieve superior Novelty performance at 40-87\% lower cost.",
    r"Small models with personas can achieve superior Novelty performance at equal or lower cost (40-87\% savings for GPT and Claude; cost parity for DeepSeek).")

# 2.5 GPT Culture_11 (d = 0.231) is not significant; do not list it among benefits
rep(r"GPT showed moderate benefits (\(d = 0.231-0.570\))",
    r"GPT showed significant small-to-medium benefits for Culture\_5 and Culture\_Expert (\(d = 0.570\) and \(0.344\))")

# 2.6 Section 3.1 still implied reliability justified the Novelty focus (and duplicated the ref)
rep(r"Based on inter-rater reliability analysis (Section 3.6), we focus our primary analysis on Novelty, the dimension central to our research question (Section 3.6).",
    r"As detailed in Section 3.6, we focus our primary analysis on Novelty, the dimension central to our research question; the other dimensions are reported as exploratory.")

# 2.7 Figure 7 (inter-rater reliability): asset existed but was never included in the draft;
#     regenerated with full-data kappas and inserted next to Table 1 in Section 3.6.3
rep("""too subjective for reliable LLM-based evaluation.}
\\end{table}""",
    """too subjective for reliable LLM-based evaluation.}
\\end{table}

\\begin{figure}[H]
\\centering
\\includegraphics[width=0.85\\textwidth]{figures_v2/figure7_inter_rater_reliability.png}
\\caption{Inter-rater reliability (Fleiss' $\\kappa$) by dimension over the full dataset (3,516 responses), at both rater grains: nine individual ratings per response (blue) and three judge-level mean ratings (green). Dashed lines mark conventional interpretation thresholds. All four core dimensions fall in the fair band (0.20--0.40); only Cultural Sensitivity falls below it.}
\\label{fig:inter_rater}
\\end{figure}""")

rep("Findings for the other dimensions are reported as exploratory given their limited reliability.",
    "Figure~\\ref{fig:inter_rater} visualizes both rater grains against the conventional interpretation thresholds. Findings for the other dimensions are reported as exploratory given their limited reliability.")

# ============ RUNNER: apply all pairs, fail loudly ============
text = SRC.read_text()
for i, (old, new) in enumerate(R):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"FATAL pair #{i}: found {n} occurrences (need exactly 1): {old[:100]!r}")
    text = text.replace(old, new)
DST.write_text(text)
print(f"OK: {len(R)} replacements applied -> {DST}")
