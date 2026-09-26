# Cultural Personas in LLMs: A Contingency Model for Novelty and Cost-Efficiency

**Repository for the paper:** *"Doing More with Less: How Cultural Personas Bridge the Cost-Performance Gap in LLMs"* 
DOI 10.5281/zenodo.19533619

---

## September 2026 Revision (v2)

**Version record:** [v2.0](https://github.com/youssef-hariri/persona-model-fit/releases/tag/v2.0) (September 26, 2026) is the current revised version. The original April 2026 version is preserved as [v1.0](https://github.com/youssef-hariri/persona-model-fit/releases/tag/v1.0).

A full statistical audit led to a revised version of the paper (same DOI: 10.5281/zenodo.19533619). The dataset is unchanged; the **unit of analysis** was corrected from the individual judge rating (pseudo-replicated) to the **response level** (N = 3,516 responses, each the mean of its nine judge ratings; 31,605 ratings total).

Key corrected headline numbers:

- Claude + Culture_5 on Novelty: Cohen's **d = 1.087** (was 0.908)
- **11 of 21** model-persona comparisons reach statistical significance after FDR correction
- No regional (East/West) moderation of persona effects (interaction **p = 0.445**)
- Inter-rater reliability on the full dataset: Fleiss' **κ = 0.31–0.33** across the four core dimensions
- Mean post-hoc power at response grain: **0.544**
- Six qualifying model-persona combinations with Efficiency Gain Ratio up to **9.15**

**New in this revision:**

| Path | Contents |
|---|---|
| `code/recompute_all.py` | Corrected response-grain pipeline (reproduces all v2 statistics) |
| `code/recompute_robustness.py` | Leave-one-out, train/test, mean-vs-median robustness checks |
| `code/generate_figures_v2.py` | Regenerates all 8 revised figures from the frozen outputs |
| `code/apply_fixes.py` | Fail-loud script that turns the original draft into the revised one (111 exact replacements) |
| `results/response_grain/` | Frozen v2 outputs (21 CSVs + run log), hashed and verified |
| `paper/` | Original and revised LaTeX sources, revised figures (`figures_v2/`), `CHANGE_LOG.md`, `DATA_MAP.md` (claim-to-data map), `SEMANTIC_MAP.md` (claim-to-evidence semantic map), `audit/` (audit memo and fix proposal) |

The root PDF (`Youssef_Hariri_doing_more_with_less_llm_personas.pdf`) is the **revised September 2026 version** (same as Zenodo, same DOI). The CSVs directly under `results/` are the **superseded rating-grain outputs**, kept as an audit trail.

To verify the correction end to end:

```bash
pip install pandas numpy scipy statsmodels scikit-learn matplotlib
python code/recompute_all.py          # recomputes every v2 statistic from data/unified_evaluations.csv
python code/recompute_robustness.py   # robustness checks
python code/generate_figures_v2.py    # regenerates the 8 revised figures
```

---

## Overview

This repository provides:

- **Prompts** for 3 cultural personas and 3 judge variations
- **100 problems** across 4 domains (Creative, General Knowledge, Instruction, Reasoning)
- **Statistical analysis code** to reproduce the paper's findings
- **Specifications** to help users generate their own data

---

## Repository Structure
Persona-model-fit/
├── README.md # This file
├── specifications/
│ ├── 01_generation_spec.pdf # LLM response generation requirements
│ ├── 02_evaluation_spec.pdf # Judge evaluation requirements
│ ├── 03_data_format_spec.pdf  # Expected CSV formats
│ └── 04_analysis_spec.pdf  # Statistical analysis requirements
├── prompts/
│ ├── 3_cultural_personas_data.jsonl # 3 cultural personas (ready to use)
│ └── 3_judges_variations.jsonl # 3 judge prompt variations
├── data/
│ ├── 100_problems.csv # 100 example problems
│ ├── unified_evaluations.csv # Full evaluations from the research experiment
│ └── llm_responses_and_evaluations # Raw responses and evaluations
├── code/
│ └── stats_with_anlysis.py # Statistical analysis code.
│ └── small_baseline_stats.py # Statistical analysis for the small baseline vs small baseline 		with persona 
│ └── recompute_all.py # v2: corrected response-grain pipeline
│ └── recompute_robustness.py # v2: robustness checks
│ └── generate_figures_v2.py # v2: figure regeneration
│ └── apply_fixes.py # v2: draft correction script
├── paper/ # v2: LaTeX sources, figures, change log, data/semantic maps, audit trail
└── results/ # Generated statistical outputs
│ └── response_grain/ # v2 frozen outputs (response-level unit of analysis)


---

## Quick Start

### Step 1: Generate LLM Responses

1. Read `specifications/01_generation_spec.md`
2. Use your preferred AI assistant to generate code for your LLM provider
3. Use `prompts/3_cultural_personas_data..jsonl` for persona definitions
4. Use `data/100_problems.csv` for the problem set
5. Run the generated code to produce responses CSV

### Step 2: Evaluate Responses

1. Read `specifications/02_evaluation_spec.md`
2. Use AI assistant to generate evaluation code for your judge models
3. Use `prompts/3_judges_variations.jsonl` for prompt variations
4. Run evaluations and collect results

### Step 3: Format Data

1. Follow `specifications/03_data_format_spec.md`
2. Combine all evaluations into `data/unified_evaluations.csv`

### Step 4: Run Analysis

```bash
# Install dependencies
pip install -r requirements.txt

# Run statistical analysis
python code/stats_with_anlysis.py

##Input Files

Personas `prompts/3_cultural_personas_data..jsonl`

Three cultural personas are provided:

ID	Name	Description
Culture_5	Innovator	Emphasizes creative autonomy, novelty, risk-taking
Culture_Expert	Implementer	Emphasizes systematic analysis, practicality, execution
Culture_11	Cultural Specialist	Emphasizes group harmony, indirect communication, cultural sensitivity
Users can add their own personas by adding new lines to this file.

Judge Variations

Three prompt variations are provided to reduce judge bias: `prompts/3_judges_variations.jsonl`

Variation	Style
var1	Standard, direct
var2	Conversational with reasoning
var3	Rubric-based with examples
Problems (data/100_problems.csv)

100 problems across four domains (25 each):

Problem IDs	Domain
0-24	Reasoning
25-49	Instruction
50-74	Creative
75-99	General Knowledge


##Output Files

Results Files (results/)

File	Contents
descriptive_stats.csv	Mean, std, count by provider and condition
effect_sizes.csv	Cohen's d with 95% bootstrap CIs (5,000 resamples)
anova_results.csv	Two-way ANOVA (Persona × Model Family)
domain_effects.csv	Effect sizes by domain
power_analysis.csv	Post-hoc statistical power
leave_one_out_sensitivity.csv	Stability analysis
economic_analysis_egr.csv	EGR, cost savings, economic value


##Interpreting Results

Metric	What It Means
Cohen's d > 0	Persona improves Novelty
Cohen's d < 0	Persona harms Novelty
|d| < 0.2	Negligible effect
0.2 ≤ |d| < 0.5	Small effect
0.5 ≤ |d| < 0.8	Medium effect
|d| ≥ 0.8	Large effect
EGR > 1	Economically viable
EGR > 5	Exceptional economic value
EGR > 10	Transformative economic value
p < 0.05	Statistically significant (after FDR correction)


##Decision Rules for Practitioners

Based on pilot results, apply these rules:

Condition	Decision
EGR > 1.5 AND performance gain > 5%	Deploy immediately
EGR > 1.5 BUT performance gain ≤ 5%	Deploy for cost-sensitive applications
EGR ≤ 1.5 BUT performance gain > 10%	Deploy for quality-critical applications
Performance gain < 0%	Reject or conduct deeper analysis
Deployment Guidelines

Phase	Action
Initial rollout	10% of traffic (canary deployment)
Monitoring period	1-2 weeks
Scale up	50% → 100% if metrics hold
Re-pilot	When models update or quarterly

##Dependencies

bash
pip install pandas numpy scipy statsmodels scikit-learn


##License

Component	License
Analysis code (code/stats.py)	MIT License
Problem data (data/100_problems.csv)	Apache 2.0
Results data	CC BY 4.0
Prompts	MIT License

##Citation

bibtex
@article{hariri2026cultural,
  title={Doing More with Less: How Cultural Personas Bridge the Cost-Performance Gap in LLMs},
  author={Hariri, Youssef},
  year={2026},
  doi={10.5281/zenodo.19533619}
}

##Contact

Email: youssef.hariri@rennes-sb.com



