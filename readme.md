# Cultural Personas in LLMs: A Contingency Model for Novelty and Cost-Efficiency

**Repository for the paper:** *"Doing More with Less: How Cultural Personas Bridge the Cost-Performance Gap in LLMs"* 
DOI 10.5281/zenodo.19533619

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
└── results/ # Generated statistical outputs


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
@article{hariri2025cultural,
  title={Doing More with Less: How Cultural Personas Bridge the Cost-Performance Gap in LLMs},
  author={Hariri, Youssef},
  year={2025}
}

##Contact

Email: youssef.hariri@rennes-sb.com



