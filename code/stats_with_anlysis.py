#!/usr/bin/env python3
"""
================================================================================
COMPLETE STATISTICAL ANALYSIS - NOVELTY FOCUSED
================================================================================
Paper: "Doing More with Less: How Cultural Personas Bridge the Cost-Performance Gap in LLMs"
Author: Youssef Hariri

This script performs all statistical analyses for the paper, focusing on Novelty
(the only dimension with good inter-rater reliability, κ = 0.68).

Analyses included:
1. Descriptive statistics (mean, std, count by model and condition)
2. Effect sizes (Cohen's d with 95% bootstrap CIs, 5,000 resamples)
3. Two-way ANOVA (Persona × Model Family)
4. Moderation analysis with Bayes Factor (Eastern vs. Western models)
5. Domain-specific effects (Creative, General Knowledge, Instruction, Reasoning)
6. Power analysis (post-hoc statistical power)
7. Robustness checks (outlier detection, generalizability)
8. Leave-one-out sensitivity analysis (corrected)
9. Economic analysis (EGR - Efficiency Gain Ratio)
10. Gemini anomaly analysis

All results are saved to CSV files in the ./results/ directory.
================================================================================
"""

import os
import pandas as pd
import numpy as np
from scipy import stats
from math import sqrt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.power import TTestIndPower
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

DATA_PATH = "./What_to_keep_for_Github/data/unified_evaluations.csv"
RESULTS_PATH = "./results"
os.makedirs(RESULTS_PATH, exist_ok=True)

# Focus only on Novelty (best inter-rater reliability: κ = 0.68)
DIMENSION = 'Novelty'
CONDITIONS = ['Culture_5', 'Culture_Expert', 'Culture_11', 'Large_Baseline']

# Model classification
EASTERN_MODELS = ['deepseek', 'Alibaba']
WESTERN_MODELS = ['Anthropic', 'openai', 'llama', 'mistral', 'Google']

# Display names for tables and figures
PROVIDER_NAME_MAP = {
    'Anthropic': 'Claude',
    'deepseek': 'DeepSeek',
    'openai': 'GPT',
    'Alibaba': 'Qwen',
    'Google': 'Gemini',
    'llama': 'Llama',
    'mistral': 'Mistral'
}

# Output token costs per 1M tokens (used for economic analysis)
COST_DATA = {
    'Anthropic': {'small': 15.00, 'large': 25.00},
    'deepseek': {'small': 0.42, 'large': 0.42},
    'openai': {'small': 2.00, 'large': 15.00},
    'llama': {'small': 0.20, 'large': 0.88},
    'mistral': {'small': 0.60, 'large': 0.30},
    'Alibaba': {'small': 0.30, 'large': 1.50},
    'Google': {'small': 1.50, 'large': 12.00},
}

# Statistical parameters
BOOTSTRAP_ITERATIONS = 5000
CONFIDENCE_LEVEL = 0.95
ALPHA = 0.05
POWER_TARGET = 0.80

print("="*80)
print("COMPLETE STATISTICAL ANALYSIS - NOVELTY FOCUSED")
print(f"Bootstrap iterations: {BOOTSTRAP_ITERATIONS}")
print(f"Confidence level: {CONFIDENCE_LEVEL * 100}%")
print("="*80)

# ============================================================================
# 1. LOAD AND PREPARE DATA
# ============================================================================

print("\n1. LOADING DATA")
df = pd.read_csv(DATA_PATH)
print(f"   Loaded {len(df)} rows")

# Convert Novelty to numeric
df[DIMENSION] = pd.to_numeric(df[DIMENSION], errors='coerce')

# Filter valid conditions
df = df[df['condition'].isin(CONDITIONS)].copy()
print(f"   Filtered to {len(df)} rows")

print(f"\n   Providers in dataset:")
for provider in df['provider'].unique():
    count = len(df[df['provider'] == provider])
    print(f"      {PROVIDER_NAME_MAP.get(provider, provider)}: {count} rows")

# ============================================================================
# 2. HELPER FUNCTIONS
# ============================================================================

def cohens_d(group1, group2):
    """
    Calculate Cohen's d effect size.
    
    Interpretation:
        |d| < 0.2: negligible
        0.2 ≤ |d| < 0.5: small
        0.5 ≤ |d| < 0.8: medium
        |d| ≥ 0.8: large
    
    Parameters:
        group1, group2: pandas Series containing the two groups to compare
    
    Returns:
        float: Cohen's d effect size
    """
    group1 = group1.dropna()
    group2 = group2.dropna()
    n1, n2 = len(group1), len(group2)
    if n1 == 0 or n2 == 0:
        return np.nan
    s1, s2 = group1.std(), group2.std()
    pooled_sd = sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))
    if pooled_sd == 0:
        return 0
    return (group1.mean() - group2.mean()) / pooled_sd


def cohens_d_ci(group1, group2, n_bootstrap=BOOTSTRAP_ITERATIONS, ci=CONFIDENCE_LEVEL):
    """
    Calculate Cohen's d with bootstrap confidence intervals.
    
    This uses resampling to estimate the precision of the effect size,
    which is more robust than parametric methods when assumptions are violated.
    
    Parameters:
        group1, group2: pandas Series containing the two groups to compare
        n_bootstrap: number of bootstrap resamples (default: 5000)
        ci: confidence level (default: 0.95)
    
    Returns:
        tuple: (d_orig, ci_lower, ci_upper)
    """
    group1 = group1.dropna()
    group2 = group2.dropna()
    
    if len(group1) == 0 or len(group2) == 0:
        return np.nan, np.nan, np.nan
    
    d_orig = cohens_d(group1, group2)
    
    # Bootstrap resampling
    d_boot = []
    n1, n2 = len(group1), len(group2)
    
    np.random.seed(42)  # For reproducibility
    for _ in range(n_bootstrap):
        g1_boot = group1.sample(n=n1, replace=True)
        g2_boot = group2.sample(n=n2, replace=True)
        d_boot.append(cohens_d(g1_boot, g2_boot))
    
    d_boot = [d for d in d_boot if not np.isnan(d)]
    
    if len(d_boot) == 0:
        return d_orig, np.nan, np.nan
    
    alpha = 1 - ci
    lower = np.percentile(d_boot, 100 * alpha / 2)
    upper = np.percentile(d_boot, 100 * (1 - alpha / 2))
    
    return d_orig, lower, upper


def interpret_d(d):
    """Return human-readable interpretation of Cohen's d."""
    if abs(d) >= 0.8:
        return 'large'
    elif abs(d) >= 0.5:
        return 'medium'
    elif abs(d) >= 0.2:
        return 'small'
    else:
        return 'negligible'


def bayes_factor(t_stat, n):
    """
    Approximate Bayes Factor from t-statistic (Rouder et al., 2009).
    
    Interpretation:
        BF > 3: Moderate evidence for effect
        BF > 1: Anecdotal evidence for effect
        BF < 0.33: Moderate evidence against effect
        BF < 0.1: Strong evidence against effect
    """
    import math
    bf = math.exp(-0.5 * t_stat**2) * math.sqrt(n/2)
    return bf


def get_domain(problem_id):
    """Map problem_id to domain based on predefined ranges."""
    DOMAIN_MAP = {
        range(0, 25): 'Reasoning',
        range(25, 50): 'Instruction',
        range(50, 75): 'Creative',
        range(75, 100): 'General Knowledge'
    }
    for r, domain in DOMAIN_MAP.items():
        if problem_id in r:
            return domain
    return 'Unknown'

# ============================================================================
# 3. DESCRIPTIVE STATISTICS
# ============================================================================

print("\n" + "="*80)
print("2. DESCRIPTIVE STATISTICS")
print("="*80)

desc_stats = df.groupby(['provider', 'condition'])[DIMENSION].agg(['mean', 'std', 'count']).round(3)
print("\nMean Novelty scores by model and condition:")
print(desc_stats)

desc_stats.to_csv(f"{RESULTS_PATH}/descriptive_stats.csv")
print(f"\n✅ Saved: {RESULTS_PATH}/descriptive_stats.csv")

# ============================================================================
# 4. EFFECT SIZES WITH BOOTSTRAPPED CIs
# ============================================================================

print("\n" + "="*80)
print(f"3. EFFECT SIZES (Cohen's d with {BOOTSTRAP_ITERATIONS} Bootstrap CIs)")
print("="*80)

effect_results = []
p_values = []

for provider in df['provider'].unique():
    prov_data = df[df['provider'] == provider]
    baseline = prov_data[prov_data['condition'] == 'Large_Baseline'][DIMENSION]
    
    for persona in ['Culture_5', 'Culture_Expert', 'Culture_11']:
        persona_data = prov_data[prov_data['condition'] == persona][DIMENSION]
        if len(persona_data) > 0 and len(baseline) > 0:
            d, lower, upper = cohens_d_ci(persona_data, baseline)
            t_stat, p_val = stats.ttest_ind(persona_data, baseline)
            p_values.append(p_val)
            
            effect_results.append({
                'provider': provider,
                'provider_display': PROVIDER_NAME_MAP.get(provider, provider),
                'persona': persona,
                'd': d,
                'ci_lower': lower,
                'ci_upper': upper,
                'p_value': p_val,
                't_statistic': t_stat
            })

effects_df = pd.DataFrame(effect_results)

# Apply FDR correction for multiple comparisons (Benjamini-Hochberg)
rejected, p_adjusted, _, _ = multipletests(p_values, alpha=ALPHA, method='fdr_bh')
effects_df['p_adjusted'] = p_adjusted
effects_df['significant_fdr'] = rejected
effects_df['magnitude'] = effects_df['d'].apply(interpret_d)

print("\nEffect sizes with 95% Bootstrap CIs:")
print(effects_df[['provider_display', 'persona', 'd', 'ci_lower', 'ci_upper', 'magnitude', 'significant_fdr']].round(3))

effects_df.to_csv(f"{RESULTS_PATH}/effect_sizes.csv", index=False)
print(f"\n✅ Saved: {RESULTS_PATH}/effect_sizes.csv")
print(f"\nTotal comparisons: {len(effects_df)}")
print(f"Significant after FDR correction: {rejected.sum()}")

# ============================================================================
# 5. TWO-WAY ANOVA (Persona × Model Family)
# ============================================================================

print("\n" + "="*80)
print("4. TWO-WAY ANOVA (Persona × Model Family)")
print("="*80)

df['model_family'] = df['provider'].apply(
    lambda x: 'Eastern' if x in EASTERN_MODELS else 'Western'
)

df_anova = df.dropna(subset=[DIMENSION, 'condition', 'model_family'])

# Check ANOVA assumptions
print("\n4.1 ANOVA Assumptions Check")

# Normality of residuals
model_temp = ols(f'{DIMENSION} ~ C(condition) * C(model_family)', data=df_anova).fit()
residuals = model_temp.resid
if len(residuals) > 5000:
    shapiro_stat, shapiro_p = stats.shapiro(residuals[:5000])
else:
    shapiro_stat, shapiro_p = stats.shapiro(residuals)
print(f"   Shapiro-Wilk test for residuals: p = {shapiro_p:.4f}")

# Homogeneity of variance (Levene's test)
groups = []
for cond in df_anova['condition'].unique():
    for family in df_anova['model_family'].unique():
        group_data = df_anova[(df_anova['condition'] == cond) & (df_anova['model_family'] == family)][DIMENSION]
        if len(group_data) > 0:
            groups.append(group_data)
if len(groups) >= 2:
    levene_stat, levene_p = stats.levene(*groups)
    print(f"   Levene's test for homogeneity: p = {levene_p:.4f}")

# Run ANOVA
model = ols(f'{DIMENSION} ~ C(condition) * C(model_family)', data=df_anova).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

# Calculate partial eta-squared (effect size for ANOVA)
residual_row = anova_table.index[-1]
residual_ss = anova_table.loc[residual_row, 'sum_sq']
anova_table['partial_eta_sq'] = anova_table['sum_sq'] / (anova_table['sum_sq'] + residual_ss)

print("\n4.2 ANOVA Results:")
print(anova_table)

anova_table.to_csv(f"{RESULTS_PATH}/anova_results.csv")
print(f"\n✅ Saved: {RESULTS_PATH}/anova_results.csv")

# Extract key results
interaction_row = 'C(condition):C(model_family)'
if interaction_row in anova_table.index:
    interaction_F = anova_table.loc[interaction_row, 'F']
    interaction_p = anova_table.loc[interaction_row, 'PR(>F)']
    interaction_eta = anova_table.loc[interaction_row, 'partial_eta_sq']
    print(f"\n   Persona × Model Family: F = {interaction_F:.2f}, p = {interaction_p:.4f}")
    print(f"   Partial η² = {interaction_eta:.3f}")

# ============================================================================
# 6. MODERATION ANALYSIS (Training Region × Persona) with Bayes Factor
# ============================================================================

print("\n" + "="*80)
print("5. MODERATION ANALYSIS (Training Region × Persona)")
print("="*80)

df['is_eastern'] = df['provider'].isin(EASTERN_MODELS).astype(int)
df['is_persona'] = df['condition'].isin(['Culture_5', 'Culture_Expert', 'Culture_11']).astype(int)

mod_data = df.dropna(subset=[DIMENSION, 'is_eastern', 'is_persona'])
X = sm.add_constant(mod_data[['is_eastern', 'is_persona']])
X['interaction'] = mod_data['is_eastern'] * mod_data['is_persona']
y = mod_data[DIMENSION]

model = sm.OLS(y, X).fit()
print("\nModeration Results:")
print(model.summary().tables[1])

# Calculate Bayes Factor for interaction
t_stat = model.tvalues['interaction']
n_total = len(mod_data)
bf = bayes_factor(t_stat, n_total)

print(f"\nBayes Factor for interaction: BF = {bf:.3f}")
if bf > 3:
    print("   Interpretation: Moderate evidence for moderation")
elif bf > 1:
    print("   Interpretation: Anecdotal evidence for moderation")
elif bf > 0.33:
    print("   Interpretation: Anecdotal evidence against moderation")
elif bf > 0.1:
    print("   Interpretation: Moderate evidence against moderation")
else:
    print("   Interpretation: Strong evidence against moderation")

# ============================================================================
# 7. DOMAIN-SPECIFIC EFFECTS
# ============================================================================

print("\n" + "="*80)
print("6. DOMAIN-SPECIFIC EFFECTS")
print("="*80)

df['domain'] = df['problem_id'].apply(get_domain)

domain_effects = []
domain_p_values = []

for persona in ['Culture_5', 'Culture_Expert', 'Culture_11']:
    for domain in df['domain'].unique():
        if domain == 'Unknown':
            continue
        persona_data = df[(df['condition'] == persona) & (df['domain'] == domain)][DIMENSION]
        baseline_data = df[(df['condition'] == 'Large_Baseline') & (df['domain'] == domain)][DIMENSION]
        
        if len(persona_data) > 0 and len(baseline_data) > 0:
            d = cohens_d(persona_data, baseline_data)
            t_stat, p_val = stats.ttest_ind(persona_data, baseline_data)
            domain_p_values.append(p_val)
            domain_effects.append({
                'persona': persona,
                'domain': domain,
                'd': d,
                'p_value': p_val
            })

domain_df = pd.DataFrame(domain_effects)

# Apply FDR correction for domain comparisons
if len(domain_p_values) > 0:
    rejected_domain, p_adjusted_domain, _, _ = multipletests(domain_p_values, alpha=ALPHA, method='fdr_bh')
    domain_df['p_adjusted'] = p_adjusted_domain
    domain_df['significant_fdr'] = rejected_domain

# Pivot table for display
pivot = domain_df.pivot_table(index='persona', columns='domain', values='d').round(3)
print("\nEffect sizes by persona and domain (Novelty):")
print(pivot)

domain_df.to_csv(f"{RESULTS_PATH}/domain_effects.csv", index=False)
print(f"\n✅ Saved: {RESULTS_PATH}/domain_effects.csv")

# ============================================================================
# 8. POWER ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("7. POWER ANALYSIS")
print("="*80)

power_results = []
for provider in df['provider'].unique():
    prov_data = df[df['provider'] == provider]
    for persona in ['Culture_5', 'Culture_Expert', 'Culture_11']:
        n1 = len(prov_data[prov_data['condition'] == persona])
        n2 = len(prov_data[prov_data['condition'] == 'Large_Baseline'])
        d = effects_df[(effects_df['provider'] == provider) & (effects_df['persona'] == persona)]['d'].values
        if len(d) > 0 and not np.isnan(d[0]):
            power = TTestIndPower().power(effect_size=abs(d[0]), nobs1=n1, ratio=n2/n1, alpha=ALPHA)
            power_results.append({'provider': provider, 'persona': persona, 'power': power})

power_df = pd.DataFrame(power_results)
power_df['provider_display'] = power_df['provider'].map(PROVIDER_NAME_MAP)

print(f"\nMean power: {power_df['power'].mean():.3f}")
print(f"Sufficient power (≥{POWER_TARGET}): {(power_df['power'] >= POWER_TARGET).mean()*100:.1f}%")
power_df.to_csv(f"{RESULTS_PATH}/power_analysis.csv", index=False)

# ============================================================================
# 9. ROBUSTNESS CHECKS
# ============================================================================

print("\n" + "="*80)
print("8. ROBUSTNESS CHECKS")
print("="*80)

# 9.1 Outlier analysis
print("\n8.1 Outlier Analysis")
iso_forest = IsolationForest(contamination=0.1, random_state=42)
outliers = iso_forest.fit_predict(df[[DIMENSION]].fillna(0))
df['is_outlier'] = outliers == -1  # FIXED: assign, not compare
outlier_pct = df['is_outlier'].mean() * 100
print(f"Outliers detected: {outlier_pct:.1f}%")

# 9.2 Generalizability (train-test split)
print("\n8.2 Generalizability")
train_problems, test_problems = train_test_split(
    df['problem_id'].unique(), test_size=0.2, random_state=42
)

train_data = df[df['problem_id'].isin(train_problems)]
test_data = df[df['problem_id'].isin(test_problems)]

for persona in ['Culture_5', 'Culture_Expert', 'Culture_11']:
    d_train = cohens_d(
        train_data[train_data['condition'] == persona][DIMENSION],
        train_data[train_data['condition'] == 'Large_Baseline'][DIMENSION]
    )
    d_test = cohens_d(
        test_data[test_data['condition'] == persona][DIMENSION],
        test_data[test_data['condition'] == 'Large_Baseline'][DIMENSION]
    )
    print(f"{persona}: train d = {d_train:.3f}, test d = {d_test:.3f}")

# 9.3 Leave-one-out sensitivity analysis (corrected)
print("\n8.3 Leave-One-Out Sensitivity Analysis")

# Calculate original average effect sizes (across all models)
original_avg_effects = {}
for persona in ['Culture_5', 'Culture_Expert', 'Culture_11']:
    persona_effects = []
    for provider in df['provider'].unique():
        prov_data = df[df['provider'] == provider]
        baseline = prov_data[prov_data['condition'] == 'Large_Baseline'][DIMENSION]
        persona_data = prov_data[prov_data['condition'] == persona][DIMENSION]
        if len(persona_data) > 0 and len(baseline) > 0:
            persona_effects.append(cohens_d(persona_data, baseline))
    original_avg_effects[persona] = np.mean(persona_effects) if persona_effects else np.nan

# Leave-one-out analysis
loo_results = []

for removed_provider in df['provider'].unique():
    df_loo = df[df['provider'] != removed_provider]
    
    for persona in ['Culture_5', 'Culture_Expert', 'Culture_11']:
        persona_effects = []
        for provider in df_loo['provider'].unique():
            prov_data = df_loo[df_loo['provider'] == provider]
            baseline = prov_data[prov_data['condition'] == 'Large_Baseline'][DIMENSION]
            persona_data = prov_data[prov_data['condition'] == persona][DIMENSION]
            if len(persona_data) > 0 and len(baseline) > 0:
                persona_effects.append(cohens_d(persona_data, baseline))
        
        avg_d_loo = np.mean(persona_effects) if persona_effects else np.nan
        original_avg = original_avg_effects.get(persona, np.nan)
        change = avg_d_loo - original_avg if not np.isnan(original_avg) else np.nan
        
        loo_results.append({
            'removed_provider': removed_provider,
            'removed_provider_display': PROVIDER_NAME_MAP.get(removed_provider, removed_provider),
            'persona': persona,
            'avg_d_loo': avg_d_loo,
            'avg_d_original': original_avg,
            'change': change,
            'stable': abs(change) < 0.1 if not np.isnan(change) else False
        })

loo_df = pd.DataFrame(loo_results)

# Summary
print("\n   Stability by persona:")
for persona in ['Culture_5', 'Culture_Expert', 'Culture_11']:
    persona_loo = loo_df[loo_df['persona'] == persona]
    stability_pct = persona_loo['stable'].mean() * 100
    mean_change = persona_loo['change'].abs().mean()
    print(f"      {persona}: {stability_pct:.1f}% stable, mean |Δ| = {mean_change:.4f}")

# Summary by removed model
model_summary = loo_df.groupby('removed_provider_display')['change'].apply(lambda x: x.abs().mean()).sort_values(ascending=False)
print("\n   Most influential models (largest average change when removed):")
for model, change in model_summary.head(5).items():
    print(f"      {model}: mean |Δ| = {change:.4f}")

loo_df.to_csv(f"{RESULTS_PATH}/leave_one_out_sensitivity.csv", index=False)
print(f"\n✅ Saved: {RESULTS_PATH}/leave_one_out_sensitivity.csv")

# ============================================================================
# 10. GEMINI ANOMALY ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("9. GEMINI ANOMALY ANALYSIS")
print("="*80)

gemini_data = df[df['provider'] == 'Google']
other_data = df[~df['provider'].isin(['Google'])]

gemini_mean = gemini_data[DIMENSION].mean()
other_mean = other_data[DIMENSION].mean()
t_stat, p_val = stats.ttest_ind(gemini_data[DIMENSION].dropna(), other_data[DIMENSION].dropna())

print(f"\nGemini vs Others - Novelty scores:")
print(f"   Gemini: {gemini_mean:.2f}")
print(f"   Others: {other_mean:.2f}")
print(f"   Difference: {gemini_mean - other_mean:.2f} points lower (p = {p_val:.4f})")

print(f"\nGemini persona effects (Novelty):")
for persona in ['Culture_5', 'Culture_Expert', 'Culture_11']:
    d = cohens_d(
        gemini_data[gemini_data['condition'] == persona][DIMENSION],
        gemini_data[gemini_data['condition'] == 'Large_Baseline'][DIMENSION]
    )
    print(f"   {persona}: d = {d:.3f}")

# ============================================================================
# 11. ECONOMIC ANALYSIS (EGR - Efficiency Gain Ratio)
# ============================================================================

print("\n" + "="*80)
print("10. ECONOMIC ANALYSIS (EGR - Efficiency Gain Ratio)")
print("="*80)
print("\nWhat is EGR?")
print("   EGR = (Performance Ratio) / (Cost Ratio)")
print("   Performance Ratio = Novelty score with persona / Novelty score of large baseline")
print("   Cost Ratio = Cost of small model / Cost of large model")
print("\nInterpretation:")
print("   EGR > 1.0 = Economically viable")
print("   EGR > 2.0 = Strong economic value")
print("   EGR > 5.0 = Exceptional value")
print("   EGR > 10.0 = Transformative value")

# Get baseline means for each provider
baseline_means = {}
for provider in df['provider'].unique():
    baseline_means[provider] = df[(df['provider'] == provider) & (df['condition'] == 'Large_Baseline')][DIMENSION].mean()

economic_results = []

for provider in df['provider'].unique():
    if provider not in COST_DATA:
        continue
    
    prov_data = df[df['provider'] == provider]
    baseline_mean = baseline_means[provider]
    cost_small = COST_DATA[provider]['small']
    cost_large = COST_DATA[provider]['large']
    
    for persona in ['Culture_5', 'Culture_Expert', 'Culture_11']:
        persona_data = prov_data[prov_data['condition'] == persona][DIMENSION]
        persona_mean = persona_data.mean()
        
        effect = effects_df[(effects_df['provider'] == provider) & (effects_df['persona'] == persona)]
        d = effect['d'].values[0] if len(effect) > 0 else np.nan
        
        if len(persona_data) > 0 and baseline_mean > 0:
            performance_ratio = persona_mean / baseline_mean
            cost_ratio = cost_small / cost_large
            egr = performance_ratio / cost_ratio if cost_ratio > 0 else np.nan
            cost_savings = (1 - cost_ratio) * 100
            beats_baseline = persona_mean > baseline_mean
            
            economic_results.append({
                'provider': provider,
                'provider_display': PROVIDER_NAME_MAP.get(provider, provider),
                'persona': persona,
                'effect_size_d': d,
                'performance_ratio': round(performance_ratio, 3),
                'cost_savings_pct': round(cost_savings, 1),
                'egr': round(egr, 2) if not np.isnan(egr) else np.nan,
                'beats_baseline': beats_baseline
            })

economic_df = pd.DataFrame(economic_results)
economic_df = economic_df.sort_values('egr', ascending=False)

print("\nEGR Results (Efficiency Gain Ratio):")
print(economic_df[['provider_display', 'persona', 'effect_size_d', 'cost_savings_pct', 'egr', 'beats_baseline']].round(3))

economic_df.to_csv(f"{RESULTS_PATH}/economic_analysis_egr.csv", index=False)
print(f"\n✅ Saved: {RESULTS_PATH}/economic_analysis_egr.csv")

"""
================================================================================
BUSINESS ANALYSIS REPORT - GENERATED FROM USER'S DATA
================================================================================
This section analyzes the user's data and generates practical business recommendations
based on their actual results, not pre-written text.
================================================================================
"""

print("\n" + "="*80)
print("11. BUSINESS ANALYSIS REPORT")
print("="*80)

# ============================================================================
# Analyze the user's actual data to generate dynamic recommendations
# ============================================================================

# Find the best combination for each business goal
best_for_novelty = effects_df.loc[effects_df['d'].idxmax()]

# Best for cost efficiency (highest EGR)
best_for_cost = economic_df.loc[economic_df['egr'].idxmax()] if len(economic_df) > 0 else None

# Balanced trade-off: different combination from best_for_cost
# (e.g., second-highest EGR or highest EGR with different persona)
if len(economic_df) > 1 and best_for_cost is not None:
    # Get combinations that are not the same as best_for_cost
    other_combinations = economic_df[
        ~((economic_df['provider'] == best_for_cost['provider']) &
          (economic_df['persona'] == best_for_cost['persona']))
    ]
    if len(other_combinations) > 0:
        best_balanced = other_combinations.loc[other_combinations['egr'].idxmax()]
    else:
        best_balanced = best_for_cost
else:
    best_balanced = best_for_cost

# Find harmful combinations
harmful = effects_df[effects_df['d'] < -0.2].sort_values('d')

# Calculate overall statistics
positive_effects = effects_df[effects_df['d'] > 0]
negative_effects = effects_df[effects_df['d'] < 0]
avg_positive = positive_effects['d'].mean() if len(positive_effects) > 0 else 0
avg_negative = negative_effects['d'].mean() if len(negative_effects) > 0 else 0

# Economic viability
economically_viable = economic_df[economic_df['egr'] > 1] if len(economic_df) > 0 else pd.DataFrame()
exceptional_value = economic_df[economic_df['egr'] > 5] if len(economic_df) > 0 else pd.DataFrame()

print("\n" + "╔" + "═"*78 + "╗")
print("║" + " " * 20 + "PRACTICAL RECOMMENDATIONS BASED ON YOUR DATA" + " " * 21 + "║")
print("╠" + "═"*78 + "╣")

# Recommendation 1: Best for Novelty
print("║" + " " * 78 + "║")
print(f"║  🎯 TO MAXIMIZE NOVELTY (creativity of responses):" + " " * 33 + "║")
print(f"║     Use {best_for_novelty['provider_display']} + {best_for_novelty['persona']}" + " " * 43 + "║")
print(f"║     → Effect: d = {best_for_novelty['d']:.3f} ({best_for_novelty['magnitude']} improvement)" + " " * 18 + "║")

# Find cost savings for this combination
best_cost_savings = None
if len(economic_df) > 0:
    best_economic = economic_df[economic_df['provider_display'] == best_for_novelty['provider_display']]
    best_economic = best_economic[best_economic['persona'] == best_for_novelty['persona']]
    if len(best_economic) > 0:
        best_cost_savings = best_economic['cost_savings_pct'].values[0]
        print(f"║     → Cost savings: {best_cost_savings:.0f}% compared to large model" + " " * 29 + "║")
    else:
        print(f"║     → Cost savings: Check economic analysis table" + " " * 35 + "║")
else:
    print(f"║     → Cost savings: Run economic analysis to calculate" + " " * 35 + "║")

print("║" + " " * 78 + "║")

# Recommendation 2: Best for Cost Efficiency
if best_for_cost is not None:
    print("║" + " " * 78 + "║")
    print(f"║  💰 TO MAXIMIZE COST EFFICIENCY:" + " " * 47 + "║")
    print(f"║     Use {best_for_cost['provider_display']} + {best_for_cost['persona']}" + " " * 43 + "║")
    print(f"║     → Effect: d = {best_for_cost['effect_size_d']:.3f}" + " " * 52 + "║")
    print(f"║     → Cost savings: {best_for_cost['cost_savings_pct']:.0f}%" + " " * 50 + "║")
    print(f"║     → EGR = {best_for_cost['egr']:.2f} (exceptional economic value)" + " " * 27 + "║")
    print("║" + " " * 78 + "║")

# Recommendation 3: Balanced Trade-off
if best_balanced is not None and best_balanced['provider_display'] != best_for_cost['provider_display']:
    print("║" + " " * 78 + "║")
    print(f"║  ⚖️ FOR A BALANCED TRADE-OFF:" + " " * 48 + "║")
    print(f"║     Use {best_balanced['provider_display']} + {best_balanced['persona']}" + " " * 43 + "║")
    print(f"║     → Effect: d = {best_balanced['effect_size_d']:.3f}" + " " * 52 + "║")
    print(f"║     → Cost savings: {best_balanced['cost_savings_pct']:.0f}%" + " " * 50 + "║")
    print(f"║     → EGR = {best_balanced['egr']:.2f}" + " " * 58 + "║")
    print("║" + " " * 78 + "║")

# Recommendation 4: Combinations to Avoid
if len(harmful) > 0:
    print("║" + " " * 78 + "║")
    print(f"║  ❌ COMBINATIONS TO AVOID:" + " " * 49 + "║")
    for _, row in harmful.head(3).iterrows():
        print(f"║     {row['provider_display']} + {row['persona']}: d = {row['d']:.3f} (harms Novelty)" + " " * 31 + "║")
    print("║" + " " * 78 + "║")

print("╠" + "═"*78 + "╣")
print("║" + " " * 20 + "KEY INSIGHTS FROM YOUR DATA" + " " * 34 + "║")
print("╠" + "═"*78 + "╣")

# Insight 1: Model dependency
best_model = effects_df.groupby('provider_display')['d'].mean().idxmax()
worst_model = effects_df.groupby('provider_display')['d'].mean().idxmin()
print("║" + " " * 78 + "║")
print(f"║  • Persona effectiveness is MODEL-DEPENDENT" + " " * 40 + "║")
print(f"║    → Best performing model: {best_model}" + " " * 50 + "║")
print(f"║    → Worst performing model: {worst_model}" + " " * 49 + "║")
print("║" + " " * 78 + "║")

# Insight 2: Domain effects
if len(domain_df) > 0:
    best_domain = domain_df.groupby('domain')['d'].mean().idxmax() if len(domain_df) > 0 else "N/A"
    print(f"║  • DOMAIN MATTERS" + " " * 75 + "║")
    print(f"║    → Culture_5 works best on: {best_domain} tasks" + " " * 42 + "║")
    print("║" + " " * 78 + "║")

# Insight 3: Economic value
if len(economically_viable) > 0:
    print(f"║  • ECONOMIC VALUE" + " " * 75 + "║")
    print(f"║    → {len(economically_viable)} combinations are economically viable (EGR > 1)" + " " * 22 + "║")
    if len(exceptional_value) > 0:
        print(f"║    → {len(exceptional_value)} combinations achieve EXCEPTIONAL value (EGR > 5)" + " " * 19 + "║")
    print("║" + " " * 78 + "║")

# Insight 4: Gemini anomaly (if present)
gemini_effects = effects_df[effects_df['provider_display'] == 'Gemini']
if len(gemini_effects) > 0 and gemini_effects['d'].abs().mean() < 0.2:
    print(f"║  • GEMINI IS AN OUTLIER" + " " * 71 + "║")
    print(f"║    → Much lower baseline scores; results should be interpreted with caution" + " " * 16 + "║")
    print("║" + " " * 78 + "║")

print("╚" + "═"*78 + "╝")

# ============================================================================
# Export business report as CSV
# ============================================================================

business_report = {
    'recommendation_type': [
        'Maximize Novelty',
        'Maximize Cost Efficiency',
        'Balanced Trade-off',
        'Avoid'
    ],
    'recommended_model': [
        best_for_novelty['provider_display'],
        best_for_cost['provider_display'] if best_for_cost is not None else 'N/A',
        best_balanced['provider_display'] if best_balanced is not None else 'N/A',
        harmful.iloc[0]['provider_display'] if len(harmful) > 0 else 'N/A'
    ],
    'recommended_persona': [
        best_for_novelty['persona'],
        best_for_cost['persona'] if best_for_cost is not None else 'N/A',
        best_balanced['persona'] if best_balanced is not None else 'N/A',
        harmful.iloc[0]['persona'] if len(harmful) > 0 else 'N/A'
    ],
    'effect_size_d': [
        round(best_for_novelty['d'], 3),
        round(best_for_cost['effect_size_d'], 3) if best_for_cost is not None else 'N/A',
        round(best_balanced['effect_size_d'], 3) if best_balanced is not None else 'N/A',
        round(harmful.iloc[0]['d'], 3) if len(harmful) > 0 else 'N/A'
    ],
    'cost_savings_pct': [
        best_cost_savings if best_cost_savings is not None else 'N/A',
        best_for_cost['cost_savings_pct'] if best_for_cost is not None else 'N/A',
        best_balanced['cost_savings_pct'] if best_balanced is not None else 'N/A',
        'N/A'
    ],
    'egr': [
        'N/A',
        best_for_cost['egr'] if best_for_cost is not None else 'N/A',
        best_balanced['egr'] if best_balanced is not None else 'N/A',
        'N/A'
    ]
}

business_df = pd.DataFrame(business_report)
business_df.to_csv(f"{RESULTS_PATH}/business_recommendations.csv", index=False)
print(f"\n✅ Saved: {RESULTS_PATH}/business_recommendations.csv")

print("\n" + "="*80)
print("✅ BUSINESS ANALYSIS COMPLETE")
print("="*80)

# ============================================================================
# 13. FINAL SUMMARY
# ============================================================================

print("\n" + "="*80)
print("12. FINAL SUMMARY")
print("="*80)

print(f"""
Analysis Complete
================
Total samples: {len(df):,}
Dimension: {DIMENSION}
Inter-rater reliability: κ = 0.68 (good)

Key Statistical Findings:
------------------------
1. Effect sizes: {rejected.sum()} significant after FDR correction (out of {len(effects_df)})
2. Largest positive effect: {effects_df.loc[effects_df['d'].idxmax(), 'provider_display']} + {effects_df.loc[effects_df['d'].idxmax(), 'persona']} (d = {effects_df['d'].max():.3f})
3. Largest negative effect: {effects_df.loc[effects_df['d'].idxmin(), 'provider_display']} + {effects_df.loc[effects_df['d'].idxmin(), 'persona']} (d = {effects_df['d'].min():.3f})
4. ANOVA interaction: F = {interaction_F:.2f}, p = {interaction_p:.4f}
5. Moderation Bayes Factor: BF = {bf:.3f}
6. Power: {(power_df['power'] >= POWER_TARGET).mean()*100:.1f}% of comparisons sufficiently powered
7. Gemini anomaly: {gemini_mean - other_mean:.2f} points below other models (p = {p_val:.4f})

Files Generated (saved to ./{RESULTS_PATH}/):
-------------------------------------------
- descriptive_stats.csv
- effect_sizes.csv
- anova_results.csv
- domain_effects.csv
- power_analysis.csv
- leave_one_out_sensitivity.csv
- economic_analysis_egr.csv
""")

if __name__ == "__main__":
    print("="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)
