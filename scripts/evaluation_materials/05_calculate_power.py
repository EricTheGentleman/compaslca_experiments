from scipy.stats import ncx2

# Replace these with values from your GLM output
beta_hat = 0.1673       # ← 'coef' column
se_beta = 0.050       # ← 'std err' column

# Noncentrality parameter
lambda_ncp = (beta_hat / se_beta) ** 2

# Compute power for alpha = 0.05 (critical chi-square = 3.84)
power = ncx2.sf(3.84, df=1, nc=lambda_ncp)

# Output
print(f"λ (noncentrality parameter): {lambda_ncp:.3f}")
print(f"Estimated statistical power: {power:.3f}")
