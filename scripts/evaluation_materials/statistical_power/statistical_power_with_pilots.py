import numpy as np
import pandas as pd
import statsmodels.formula.api as smf



def estimate_power_with_lrt(sample_sizes, effect_sizes, n_factors=6, n_sims=50, alpha=0.05):
    results = []

    for n in sample_sizes:
        sig_count = np.zeros(n_factors)
        
        for _ in range(n_sims):
            df = simulate_factorial_data(n_samples=n, n_factors=n_factors, effect_sizes=effect_sizes)
            
            # Full model
            formula_full = "Y ~ " + " + ".join([f'X{i+1}' for i in range(n_factors)])
            model_full = smf.glm(formula_full, data=df, family=smf.families.Binomial()).fit()
            
            # Test each factor with likelihood ratio test
            for i in range(n_factors):
                # Reduced model without factor i+1
                predictors = [f'X{j+1}' for j in range(n_factors) if j != i]
                formula_reduced = "Y ~ " + " + ".join(predictors) if predictors else "Y ~ 1"
                model_reduced = smf.glm(formula_reduced, data=df, family=smf.families.Binomial()).fit()
                
                # LRT statistic
                lrt = 2 * (model_full.llf - model_reduced.llf)
                p_value = 1 - scipy.stats.chi2.cdf(lrt, 1)
                
                if p_value < alpha:
                    sig_count[i] += 1
        
        power = sig_count / n_sims
        results.append({"sample_size": n, "power_by_factor": power, "avg_power": power.mean()})

    return results


def simulate_factorial_data(n_samples=2191, 
                            n_factors=6, 
                            base_prob=0.523, 
                            effect_sizes=None, 
                            seed=123):
    np.random.seed(seed)
    if effect_sizes is None:
        effect_sizes = [np.log(2)] * n_factors  # Default odds ratio = 2

    # Binary (0/1) predictors
    X = np.random.randint(0, 2, size=(n_samples, n_factors))
    df = pd.DataFrame(X, columns=[f'X{i+1}' for i in range(n_factors)])

    # Compute log-odds
    base_logit = np.log(base_prob / (1 - base_prob))
    logits = base_logit + np.dot(X, effect_sizes)

    # Probabilities
    probs = 1 / (1 + np.exp(-logits))

    # Binary outcome
    df["Y"] = np.random.binomial(1, probs)

    return df


def estimate_power(sample_sizes, odds_ratio=2.0, n_factors=6, n_sims=50, alpha=0.05):
    results = []

    for n in sample_sizes:
        sig_count = 0
        for _ in range(n_sims):
            df = simulate_factorial_data(
                n_samples=n,
                n_factors=n_factors,
                effect_sizes=[np.log(odds_ratio)] * n_factors
            )

            # Fit logistic regression
            formula = "Y ~ " + " + ".join([f'X{i+1}' for i in range(n_factors)])
            model = smf.glm(formula, data=df, family=smf.families.Binomial()).fit()

            # Check if any p-values < alpha
            pvalues = model.pvalues[1:]  # exclude intercept
            if any(p < alpha for p in pvalues):
                sig_count += 1

        power = sig_count / n_sims
        results.append({"sample_size": n, "estimated_power": power})

    return pd.DataFrame(results)


# Use your empirically estimated effect size per variable:
empirical_log_odds = # INSERT HERE FROM GENERALIZED LINEAR MODEL RESULTS
effect_sizes = [empirical_log_odds] * 6

# After fitting the GLM to pilot data
coefficients = model.params[1:]  # Exclude intercept
min_effect = coefficients.min()
avg_effect = coefficients.mean()
max_effect = coefficients.max()

print(f"Minimum effect: {min_effect}")
print(f"Average effect: {avg_effect}")
print(f"Maximum effect: {max_effect}")

# Run power analysis with different effect size scenarios
power_min = estimate_power(
    sample_sizes=[100, 150, 200, 250, 300],
    odds_ratio=np.exp(min_effect),
    n_factors=6,
    n_sims=1000,
    alpha=0.05
)

power_avg = estimate_power(
    sample_sizes=[100, 150, 200, 250, 300],
    odds_ratio=np.exp(avg_effect),
    n_factors=6,
    n_sims=1000,
    alpha=0.05
)

# Consider a more conservative estimate (e.g., 80% of minimum)
power_conservative = estimate_power(
    sample_sizes=[100, 150, 200, 250, 300],
    odds_ratio=np.exp(min_effect * 0.8),
    n_factors=6,
    n_sims=1000,
    alpha=0.05
)
print(f"power min: {power_min}")
print(f"power avg:  {power_avg}")
print(f"power conservative:  {power_conservative}")
