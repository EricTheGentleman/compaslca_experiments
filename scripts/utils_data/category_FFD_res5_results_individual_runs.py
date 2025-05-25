import os
import json
import pandas as pd
from pathlib import Path

# === CONFIGURATION ===
ground_truth_base = Path(r"data/input/category_test/ground_truth/gt_test")
runs_base = Path(r"data/output/category/01_samples_test/runs")
output_csv_dir = Path(r"data/output/category/01_samples_test/runs_csv")  # Save CSVs inside each run folder or you can choose a separate dir

subfolders = ["Elements", "Target_Layers"]  # Relevant subfolders in both base dirs

# === Load Ground Truth Categories ===
ground_truth = {}

for subfolder in subfolders:
    gt_path = os.path.join(ground_truth_base, subfolder)
    for filename in os.listdir(gt_path):
        if filename.endswith(".json"):
            full_path = os.path.join(gt_path, filename)
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                ground_truth[filename] = data.get("category", "")

# === Process Each Run ===
for run_name in os.listdir(runs_base):
    run_path = os.path.join(runs_base, run_name)
    if not os.path.isdir(run_path) or not run_name.startswith("run_"):
        continue

    results = []

    for subfolder in subfolders:
        run_subdir = os.path.join(run_path, subfolder)
        if not os.path.isdir(run_subdir):
            continue

        for filename in os.listdir(run_subdir):
            if not filename.endswith(".json"):
                continue

            gt_category = ground_truth.get(filename, None)
            if gt_category is None:
                continue  # File not found in ground truth

            file_path = os.path.join(run_subdir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    matched_category = data.get("llm_response", {}).get("Matched Category", "")
                    match = int(matched_category.strip() == gt_category.strip())
                    results.append({"filename": filename, "match": match})
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    # Save CSV
    df = pd.DataFrame(results)
    csv_output_path = os.path.join(output_csv_dir, f"{run_name}.csv")
    df.to_csv(csv_output_path, index=False)
    print(f"Saved: {csv_output_path}")
