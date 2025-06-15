import os
import json
import pandas as pd
import unicodedata
from pathlib import Path

# === CONFIGURATION ===
ground_truth_base = Path(r"data/input/category_test/ground_truth/gt_holdout")
runs_base = Path(r"data/output/category/02_samples_holdout/runs")
output_csv_dir = Path(r"data/output/category/02_samples_holdout/runs_csv")

subfolders = ["Elements", "Target_Layers"]

# === Load Ground Truth Categories ===
ground_truth = {}
for subfolder in subfolders:
    gt_path = os.path.join(ground_truth_base, subfolder)
    for filename in os.listdir(gt_path):
        if filename.endswith(".json"):
            full_path = os.path.join(gt_path, filename)
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                norm_filename = unicodedata.normalize("NFC", filename)
                ground_truth[norm_filename] = data.get("category", "")

# === Counters for debugging ===
total_processed = 0
skipped_no_gt = 0
skipped_invalid_json = 0
skipped_missing_subdir = 0
skipped_no_matched_category = 0

# === Process Each Run ===
for run_name in os.listdir(runs_base):
    run_path = os.path.join(runs_base, run_name)
    if not os.path.isdir(run_path):
        continue

    results = []

    for subfolder in subfolders:
        run_subdir = os.path.join(run_path, subfolder)
        if not os.path.isdir(run_subdir):
            print(f"Skipped missing subfolder: {run_subdir}")
            skipped_missing_subdir += 1
            continue

        for filename in os.listdir(run_subdir):
            if not filename.endswith(".json"):
                continue

            norm_filename = unicodedata.normalize("NFC", filename)
            gt_category = ground_truth.get(norm_filename, None)
            if gt_category is None:
                print(f"Skipped: Ground truth not found for {filename}")
                skipped_no_gt += 1
                continue

            # Inside the for loop over files
            file_path = os.path.join(run_subdir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    matched_category = data.get("llm_response", {}).get("Matched Category", "")
                    if not matched_category:
                        print(f"Skipped: 'Matched Category' missing in {file_path}")
                        skipped_no_matched_category += 1
                        continue

                    match = int(matched_category.strip() == gt_category.strip())
                    processing_time = data.get("llm_metadata", {}).get("processing_time", None)
                    cost = data.get("llm_metadata", {}).get("inference_cost_usd", None)

                    results.append({
                        "filename": filename,
                        "match": match,
                        "Processing Time": processing_time,
                        "Cost": cost
                    })
                    total_processed += 1
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    skipped_invalid_json += 1

    # Save CSV
    df = pd.DataFrame(results)
    if not output_csv_dir.exists():
        output_csv_dir.mkdir(parents=True)
    csv_output_path = os.path.join(output_csv_dir, f"{run_name}.csv")
    df.to_csv(csv_output_path, index=False)
    print(f"Saved: {csv_output_path} with {len(df)} rows")

# === Summary ===
print("\n=== Debug Summary ===")
print(f"Total processed files: {total_processed}")
print(f"Skipped due to missing ground truth: {skipped_no_gt}")
print(f"Skipped due to invalid JSON: {skipped_invalid_json}")
print(f"Skipped due to missing subfolders: {skipped_missing_subdir}")
print(f"Skipped due to missing 'Matched Category': {skipped_no_matched_category}")
