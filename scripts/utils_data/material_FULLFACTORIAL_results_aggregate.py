from pathlib import Path
import pandas as pd

# === CONFIGURATION ===
template_csv_path = Path("data/output/material/01_samples_test/material_test_matrix_FFD_full.csv")
runs_results_dir = Path("data/output/material/01_samples_test/runs_csv")
output_csv_path = Path("data/output/material/01_samples_test/material_test_runs_aggregated.csv")

# === Load Template CSV ===
df_template = pd.read_csv(template_csv_path)

# Prepare new columns
df_template["mean_f1_score"] = None
df_template["mean_f0.5_score"] = None
df_template["std_f1_score"] = None
df_template["std_f0.5_score"] = None
df_template["count_fscore_1.0"] = None
df_template["count_fscore_0.0"] = None
df_template["count_fscore_continuous"] = None

# === Process Each Per-Run F-score CSV ===
for csv_file in runs_results_dir.glob("run_*.csv"):
    run_id = csv_file.stem.split("_")[1]  # Extract numeric part
    run_label = f"run_{run_id}"

    if run_label not in df_template["Run"].values:
        print(f"Warning: {run_label} not found in template. Skipping.")
        continue

    df_run = pd.read_csv(csv_file)
    if "f1_score" not in df_run.columns or "f0.5_score" not in df_run.columns:
        print(f"Warning: F-score columns missing in {csv_file.name}. Skipping.")
        continue

    f1 = df_run["f1_score"].dropna()
    f05 = df_run["f0.5_score"].dropna()

    stats = {
        "mean_f1_score": f1.mean(),
        "mean_f0.5_score": f05.mean(),
        "std_f1_score": f1.std(),
        "std_f0.5_score": f05.std(),
        "count_fscore_1.0": (f1 == 1.0).sum(),
        "count_fscore_0.0": (f1 == 0.0).sum(),
        "count_fscore_continuous": ((f1 > 0.0) & (f1 < 1.0)).sum()
    }

    for key, value in stats.items():
        df_template.loc[df_template["Run"] == run_label, key] = value

# === Save Aggregated Template ===
df_template.to_csv(output_csv_path, index=False)
print(f"Aggregated F-score summary saved to: {output_csv_path}")
