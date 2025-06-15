from pathlib import Path
import pandas as pd

# === CONFIGURATION ===
runs_results_dir = Path("data/output/category/02_samples_holdout/runs_csv")  # Folder containing per-run CSVs
output_csv_path = Path("data/output/category/02_samples_holdout/category_holdout_aggregated.csv")  # Output CSV

# === Prepare Aggregation ===
aggregated_rows = []

for csv_file in runs_results_dir.glob("*.csv"):
    model_name = csv_file.stem 

    df_run = pd.read_csv(csv_file)

    if "match" not in df_run.columns:
        print(f"Warning: 'match' column missing in {csv_file.name}. Skipping.")
        continue

    match_values = df_run["match"].dropna()
    cost_values = df_run["Cost"].dropna()
    duration_values = df_run["Processing Time"].dropna()

    aggregated_rows.append({
        "model": model_name,
        "mean": match_values.mean(),
        "std_dev": match_values.std(),
        "min": match_values.min(),
        "max": match_values.max(),
        "freq_0": (match_values == 0).sum(),
        "freq_1": (match_values == 1).sum(),
        "accuracy_percent": 100 * match_values.mean(),
        "Avg. Cost": cost_values.mean(),
        "Avg. Duration": duration_values.mean()
    })

# === Save Aggregated CSV ===
df_aggregated = pd.DataFrame(aggregated_rows)
df_aggregated.to_csv(output_csv_path, index=False)
print(f"Aggregated results saved to: {output_csv_path}")
