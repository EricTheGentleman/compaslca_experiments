import statsmodels.api as sm
import pandas as pd

# === 1. Load the CSV ===
csv_path = "data/output/material/00_pilot_data/pilot_data.csv"  # Update path if needed
df = pd.read_csv(csv_path)

# === 2. Create response variable: [successes, failures] ===
df['failures'] = df['trials'] - df['f0.5_success']  # or use 'f0.5_success' if analyzing that

# === 3. Define predictor variables (independent variables) ===
# Use all 6 parameters
X = df[['geo', 'ger', 'cot', 'etr', 'isr', 'exp']]
X = sm.add_constant(X)  # Add intercept

# === 4. Define response matrix ===
y = df[['f0.5_success', 'failures']] #df[['f1_success', 'failures']]

# === 5. Fit the GLM ===
model = sm.GLM(y, X, family=sm.families.Binomial())
results = model.fit()

# === 6. Output results ===
output_path = "data/output/material/00_pilot_data/f05_glm_summary_pilot.txt"  # You can change this to .log or .md if preferred

with open(output_path, "w", encoding="utf-8") as f:
    f.write(results.summary().as_text())


print(f"GLM summary saved to: {output_path}")

