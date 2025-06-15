from pathlib import Path
import pandas as pd

# === CONFIGURATION ===
runs_results_dir = Path("data/output/material/02_samples_holdout/runs_csv")
output_csv_path = Path("data/output/material/02_samples_holdout/material_holdout_runs_aggregated.csv")

# === Initialize empty list to collect all stats ===
rows = []

# === Process Each Per-Run F-score CSV ===
for csv_file in runs_results_dir.glob("*.csv"):
    model_name = csv_file.stem  # e.g., "openai_GPT_4o"

    df_run = pd.read_csv(csv_file)
    if "f1_score" not in df_run.columns or "f0.5_score" not in df_run.columns:
        print(f"Warning: F-score columns missing in {csv_file.name}. Skipping.")
        continue

    f1 = df_run["f1_score"].dropna()
    f05 = df_run["f0.5_score"].dropna()
    cost = df_run["Cost"]
    entries = df_run["Entries Count"]
    time = df_run["Processing Time"]

    row = {
        "model": model_name,
        "mean_f1_score": f1.mean(),
        "mean_f0.5_score": f05.mean(),
        "std_f1_score": f1.std(),
        "std_f0.5_score": f05.std(),
        "count_fscore_1.0": (f1 == 1.0).sum(),
        "count_fscore_0.0": (f1 == 0.0).sum(),
        "count_fscore_continuous": ((f1 > 0.0) & (f1 < 1.0)).sum(),
        "avg. entries": entries.mean(),
        "avg. cost": cost.mean(),
        "avg. time": time.mean()
    }

    rows.append(row)

# === Combine into final DataFrame and save ===
df_summary = pd.DataFrame(rows)
df_summary = df_summary.sort_values("model").reset_index(drop=True)
df_summary.to_csv(output_csv_path, index=False)
print(f"Aggregated F-score summary saved to: {output_csv_path}")
