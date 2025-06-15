import pandas as pd

# Directly use the file path
file_path = "data/output/material/02_samples_holdout/material_holdout_runs_aggregated.csv"

# Read the CSV file
df = pd.read_csv(file_path)

# Check if the required columns exist
if "model" not in df.columns or "mean_f0.5_score" not in df.columns:
    raise ValueError("CSV must contain 'model' and 'mean_f0.5_score' columns.")

# Sort by mean_f0.5_score in ascending order
sorted_df = df.sort_values(by="mean_f0.5_score", ascending=True)

# Print the model names in order
print("\nModels ordered by mean_f0.5_score (lowest to highest):")
for model in sorted_df["model"]:
    print(model)

