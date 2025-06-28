from pathlib import Path
import pandas as pd

# === CONFIGURATION ===
template_csv_path = Path("data/output/category/01_samples_test/category_test_matrix.csv")  # e.g., data/input/template.csv
runs_results_dir = Path("data/output/category/01_samples_test/runs_csv")  # e.g., data/output/category/01_samples_test/runs
output_csv_path = Path("data/output/category/01_samples_test/category_test_runs_aggregated.csv")  # You choose the output location

# === Load Template CSV ===
df_template = pd.read_csv(template_csv_path)

# Prepare new columns
df_template["mean"] = None
df_template["std_dev"] = None
df_template["min"] = None
df_template["max"] = None
df_template["freq_0"] = None
df_template["freq_1"] = None
df_template["accuracy_percent"] = None

# === Process Each Per-Run CSV ===
for csv_file in runs_results_dir.glob("run_*.csv"):
    run_id = csv_file.stem.split("_")[1]  # Extract numeric part
    run_label = f"run_{run_id}"  # Format like "run_9"

    if run_label not in df_template["Run"].values:
        print(f"Warning: {run_label} not found in template. Skipping.")
        continue

    df_run = pd.read_csv(csv_file)
    if "match" not in df_run.columns:
        print(f"Warning: 'match' column missing in {csv_file.name}. Skipping.")
        continue

    match_values = df_run["match"].dropna()

    stats = {
        "mean": match_values.mean(),
        "std_dev": match_values.std(),
        "min": match_values.min(),
        "max": match_values.max(),
        "freq_0": (match_values == 0).sum(),
        "freq_1": (match_values == 1).sum(),
        "accuracy_percent": 100 * match_values.mean()
    }

    for key, value in stats.items():
        df_template.loc[df_template["Run"] == run_label, key] = value

# === Save Aggregated Template ===
df_template.to_csv(output_csv_path, index=False)
print(f"Aggregated template saved to: {output_csv_path}")
