"""
Small Baseline vs. Small+Persona Analysis
For Appendix - Pure Persona Effects on Novelty

Usage: python small_baseline_analysis.py
"""
import os
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

DATA_PATH = "./What_to_keep_for_Github/data/unified_evaluations.csv"
RESULTS_PATH = "./results"
os.makedirs(RESULTS_PATH, exist_ok=True)

DIMENSION = 'Novelty'
CONDITIONS = ['Small_Baseline', 'Culture_5', 'Culture_Expert', 'Culture_11']

PROVIDER_NAME_MAP = {
    'Anthropic': 'Claude',
    'deepseek': 'DeepSeek',
    'openai': 'GPT',
    'Alibaba': 'Qwen',
    'Google': 'Gemini',
    'llama': 'Llama',
    'mistral': 'Mistral'
}

ALPHA = 0.05

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def cohens_d(group1, group2):
    """Calculate Cohen's d effect size."""
    group1 = group1.dropna()
    group2 = group2.dropna()
    n1, n2 = len(group1), len(group2)
    if n1 == 0 or n2 == 0:
        return np.nan
    s1, s2 = group1.std(), group2.std()
    pooled_sd = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))
    if pooled_sd == 0:
        return 0
    return (group1.mean() - group2.mean()) / pooled_sd

def interpret_d(d):
    """Interpret Cohen's d magnitude."""
    if abs(d) >= 0.8:
        return 'large'
    elif abs(d) >= 0.5:
        return 'medium'
    elif abs(d) >= 0.2:
        return 'small'
    else:
        return 'negligible'

# ============================================================================
# LOAD DATA
# ============================================================================

print("="*60)
print("SMALL BASELINE VS. SMALL+PERSONA ANALYSIS")
print("="*60)

df = pd.read_csv(DATA_PATH)
print(f"Loaded {len(df)} rows")

# Convert Novelty to numeric
df[DIMENSION] = pd.to_numeric(df[DIMENSION], errors='coerce')

# Filter to relevant conditions
df = df[df['condition'].isin(CONDITIONS)].copy()
print(f"Filtered to {len(df)} rows (Small_Baseline + personas)")

# ============================================================================
# CALCULATE STATISTICS
# ============================================================================

results = []

for provider in df['provider'].unique():
    # Get small baseline for this provider
    baseline = df[(df['provider'] == provider) & (df['condition'] == 'Small_Baseline')][DIMENSION]
    
    if len(baseline) == 0:
        print(f"Warning: No Small_Baseline for {provider}")
        continue
    
    for persona in ['Culture_5', 'Culture_Expert', 'Culture_11']:
        persona_data = df[(df['provider'] == provider) & (df['condition'] == persona)][DIMENSION]
        
        if len(persona_data) == 0:
            continue
        
        # Calculate statistics
        d = cohens_d(persona_data, baseline)
        t_stat, p_val = stats.ttest_ind(persona_data, baseline, equal_var=False)
        diff = persona_data.mean() - baseline.mean()
        
        results.append({
            'provider': provider,
            'provider_display': PROVIDER_NAME_MAP.get(provider, provider),
            'persona': persona,
            'baseline_mean': round(baseline.mean(), 2),
            'persona_mean': round(persona_data.mean(), 2),
            'diff': round(diff, 2),
            'cohens_d': round(d, 3),
            'p_value': p_val,
            'n_baseline': len(baseline),
            'n_persona': len(persona_data)
        })

# Create DataFrame
results_df = pd.DataFrame(results)

# FDR correction for multiple comparisons
p_vals = results_df['p_value'].values
rejected, p_adjusted, _, _ = multipletests(p_vals, alpha=ALPHA, method='fdr_bh')
results_df['p_adjusted'] = p_adjusted
results_df['significant_fdr'] = rejected
results_df['magnitude'] = results_df['cohens_d'].apply(interpret_d)

# ============================================================================
# PRINT RESULTS
# ============================================================================

print("\n" + "="*60)
print("RESULTS: Small Baseline vs. Small+Persona")
print("="*60)

print("\n{:<12} {:<14} {:>12} {:>12} {:>10} {:>10} {:>8}".format(
    "Model", "Persona", "Baseline", "Persona", "Cohen's d", "Magnitude", "Sig."
))
print("-"*80)

for _, row in results_df.iterrows():
    sig = "*" if row['significant_fdr'] else ""
    print("{:<12} {:<14} {:>12.2f} {:>12.2f} {:>10.3f}{} {:>10}".format(
        row['provider_display'],
        row['persona'].replace('_', ' '),
        row['baseline_mean'],
        row['persona_mean'],
        row['cohens_d'],
        sig,
        row['magnitude']
    ))

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

print("\n" + "="*60)
print("SUMMARY")
print("="*60)

n_positive = len(results_df[results_df['cohens_d'] > 0])
n_negative = len(results_df[results_df['cohens_d'] < 0])
n_significant = results_df['significant_fdr'].sum()

print(f"Total comparisons: {len(results_df)}")
print(f"Positive effects (d > 0): {n_positive} ({n_positive/len(results_df)*100:.1f}%)")
print(f"Negative effects (d < 0): {n_negative} ({n_negative/len(results_df)*100:.1f}%)")
print(f"Significant after FDR: {n_significant} ({n_significant/len(results_df)*100:.1f}%)")

# Best and worst
best = results_df.loc[results_df['cohens_d'].idxmax()]
worst = results_df.loc[results_df['cohens_d'].idxmin()]

print(f"\nLargest positive effect: {best['provider_display']} + {best['persona']} (d = {best['cohens_d']:.3f})")
print(f"Largest negative effect: {worst['provider_display']} + {worst['persona']} (d = {worst['cohens_d']:.3f})")

# ============================================================================
# SAVE TO CSV
# ============================================================================

output_cols = ['provider_display', 'persona', 'baseline_mean', 'persona_mean',
               'cohens_d', 'ci_lower', 'ci_upper', 'magnitude', 'significant_fdr',
               'n_baseline', 'n_persona']

results_df.to_csv(f"{RESULTS_PATH}/small_baseline_vs_persona.csv", index=False)
print(f"\n✅ Saved: {RESULTS_PATH}/small_baseline_vs_persona.csv")

# ============================================================================
# GENERATE LATEX TABLE FOR APPENDIX
# ============================================================================

latex = """\\begin{table}[H]
\\centering
\\caption{Pure Persona Effects (Small Baseline vs. Small+Persona) for Novelty}
\\label{tab:pure_persona}
\\begin{tabular}{llccc}
\\toprule
Model & Persona & Baseline Mean & Persona Mean & Cohen's d \\\\
\\midrule
"""

for _, row in results_df.iterrows():
    sig = "$^*$" if row['significant_fdr'] else ""
    latex += f"{row['provider_display']} & {row['persona'].replace('_', ' ')} & "
    latex += f"{row['baseline_mean']:.2f} & {row['persona_mean']:.2f} & "
    latex += f"{row['cohens_d']:.3f}{sig} \\\\\n"

latex += """\\bottomrule
\\end{tabular}
\\caption*{\\footnotesize $^*$p < 0.05 (FDR-corrected). Positive Cohen's d indicates improvement from persona.}
\\end{table}
"""

with open(f"{RESULTS_PATH}/small_baseline_vs_persona_table.tex", 'w') as f:
    f.write(latex)

print(f"✅ Saved: {RESULTS_PATH}/small_baseline_vs_persona_table.tex")

# ============================================================================
# PRINT LATEX TABLE FOR COPY/PASTE
# ============================================================================

print("\n" + "="*60)
print("LATEX TABLE (Copy to Appendix)")
print("="*60)
print(latex)

print("\n" + "="*60)
print("✅ ANALYSIS COMPLETE")
print("="*60)
