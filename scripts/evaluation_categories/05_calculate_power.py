import numpy as np
from scipy.stats import ncx2
from scipy.optimize import fsolve

# --- Core Formula ---
def estimate_se_logit(n_total, p_mean=0.6, f_j = 0.5):
    """
    Estimate standard error for a coefficient in logistic regression
    with binary predictors in a balanced factorial design (f_j = 0.5)
    """
    var_y = p_mean * (1 - p_mean)
    fisher_info = n_total * var_y * (f_j*(1-f_j))
    return 1 / np.sqrt(fisher_info)

# --- Solve for minimum detectable effect ---
def solve_mde(n_total, p_mean=0.6, var_x=0.25, power=0.8, alpha=0.05):
    se = estimate_se_logit(n_total, p_mean, var_x)
    crit_chi = 3.84  # crit chi depends on alpha and degrees of freedom

    def equation(beta):
        lambda_ncp = (beta / se) ** 2
        return ncx2.sf(crit_chi, df=1, nc=lambda_ncp) - power

    return fsolve(equation, x0=0.1)[0]

# --- Solve for required sample size ---
def solve_sample_size(beta, runs, p_mean=0.6, var_x=0.25, power=0.8, alpha=0.05):
    crit_chi = 3.84 # crit chi depends on alpha and degrees of freedom

    def equation(n):
        se = estimate_se_logit(n, p_mean, var_x)
        lambda_ncp = (beta / se) ** 2
        return ncx2.sf(crit_chi, df=1, nc=lambda_ncp) - power

    return (fsolve(equation, x0=1000)[0])/runs

# === EXAMPLES ===

# Example 1: Solve for MDE given sample size
n_runs = 64 # amount of runs
n_samples = 191 # amount of samples
n_total = n_runs * n_samples # e.g., 64 conditions × 191 per condition
p_mean = 0.6 # average outcome probability, based on pilots
mde = solve_mde(n_total)
print(f"Minimum detectable log-odds effect at 80% power: {mde:.4f}")

# Example 2: Solve for required sample size to detect effect = 0.14
required_n = solve_sample_size(beta=0.14, runs=n_runs)
print(f"Required sample size to detect β = 0.14 with 80% power: {required_n:.0f}")
