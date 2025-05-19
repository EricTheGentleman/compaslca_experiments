import numpy as np
import pandas as pd
import itertools
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy.stats import chi2

# -----------------------------
# 0. PILOT-BASED CHANGES
# -----------------------------

"""
These are empirically observed probabilities of the outcome from a pilot study.
logit_off is the log-odds of the outcome when all predictors are 0
logit_on is the log-odds when all predictors are 1
delta_logit gives the combined log-odds increase when all predictors are turned on.
Provides a target effect budget for the simulated effects of individual predictors
"""

p_off = 0.523 # all_predictors_off
p_on = 0.675 # all_predictors_on
logit_off = np.log(p_off / (1 - p_off))
logit_on  = np.log(p_on / (1 - p_on))
delta_logit = logit_on - logit_off


# -----------------------------
# 1. PILOT-BASED COEFFICIENT SETUP
# -----------------------------

"The raw betas come from the pilot but are confounded due to the 4 runs"
"They are normalized to a maximum weight, turning them into relative importance weights"
"Then manually, some of the weights are adjusted"


# Raw coefficients from pilot (confounded)
raw_betas = {
    'geo': 0.0487,
    'ger': 0.1673,
    'cot': 0.0487,
    'etr': 0.1673,
    'isr': 0.0487,
    'exp': 0.1673
}

# Normalize to max = 1 and manually tweak weights
max_raw = max(raw_betas.values())
relative_weights = {k: v / max_raw for k, v in raw_betas.items()}

# Domain-informed adjustments
relative_weights['exp'] = 1.2   # assume exp has more influence
relative_weights['etr'] = 0.9   # etr slightly less
# leave others as is

# Set max desired log-odds effect (based on domain, ~35% OR increase)
max_effect = 0.2
effect_sizes = {k: v * max_effect for k, v in relative_weights.items()}


# -----------------------------
# 2. SIMULATION FUNCTION
# -----------------------------

def simulate_data(n_per_run=191, effect_sizes=None, seed=None, baseline_prob=0.523):
    if seed is not None:
        np.random.seed(seed)

    factors = list(effect_sizes.keys())
    # Full factorial: all 2^k combinations
    runs = [dict(zip(factors, vals)) for vals in itertools.product([0, 1], repeat=len(factors))]

    df = []
    base_logit = np.log(baseline_prob / (1 - baseline_prob))

    for row in runs:
        logit = base_logit + sum(row[var] * effect_sizes[var] for var in effect_sizes)
        prob = 1 / (1 + np.exp(-logit))
        y = np.random.binomial(1, prob, size=n_per_run)
        for val in y:
            df.append({**row, 'Y': val})
    return pd.DataFrame(df)


# -----------------------------
# 3. MODEL FITTING + TESTS
# -----------------------------

def run_model_tests(df, test_var='geo'):
    predictors = ['geo', 'ger', 'cot', 'etr', 'isr', 'exp']
    formula_full = "Y ~ " + " + ".join(predictors)
    predictors_reduced = [p for p in predictors if p != test_var]
    formula_reduced = "Y ~ " + " + ".join(predictors_reduced)

    # Fit full and reduced models
    model_full = smf.glm(formula_full, data=df, family=sm.families.Binomial()).fit()
    model_reduced = smf.glm(formula_reduced, data=df, family=sm.families.Binomial()).fit()

    # Likelihood Ratio Test (LRT)
    lr_stat = 2 * (model_full.llf - model_reduced.llf)
    p_lr = 1 - chi2.cdf(lr_stat, df=1)

    # Wald Test (using standard error from full model)
    wald_stat = (model_full.params[test_var] / model_full.bse[test_var]) ** 2
    p_wald = 1 - chi2.cdf(wald_stat, df=1)

    return {
        "beta": model_full.params[test_var],
        "se": model_full.bse[test_var],
        "p_lr": p_lr,
        "p_wald": p_wald
    }


# -----------------------------
# 4. POWER SIMULATION LOOP
# -----------------------------

def power_analysis(n_reps=500, alpha=0.05, test_var='geo'):
    significant_lr = 0
    significant_wald = 0
    beta_vals, se_vals = [], []

    for i in range(n_reps):
        df_sim = simulate_data(effect_sizes=effect_sizes, seed=i)
        results = run_model_tests(df_sim, test_var=test_var)

        if results['p_lr'] < alpha:
            significant_lr += 1
        if results['p_wald'] < alpha:
            significant_wald += 1

        beta_vals.append(results['beta'])
        se_vals.append(results['se'])

    return {
        "power_lr": significant_lr / n_reps,
        "power_wald": significant_wald / n_reps,
        "avg_beta": np.mean(beta_vals),
        "avg_se": np.mean(se_vals)
    }


# -----------------------------
# 5. RUN POWER ANALYSIS
# -----------------------------

if __name__ == "__main__":
    # Run power analysis for the variable 'geo'
    results = power_analysis(n_reps=500, test_var='etr')

    print("\n=== POWER ANALYSIS RESULTS ===")
    print(f"Power (LRT):   {results['power_lr']:.3f}")
    print(f"Power (Wald):  {results['power_wald']:.3f}")
    print(f"Avg Beta:      {results['avg_beta']:.4f}")
    print(f"Avg Std Error: {results['avg_se']:.4f}")
