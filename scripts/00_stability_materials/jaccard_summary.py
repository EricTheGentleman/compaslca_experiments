import csv
import json
from statistics import mean, median
from pathlib import Path

# --- CONFIGURATION ---
csv_path = Path("data/output/material/00_stability/jaccard_summary_materials.csv")  # Update this path!
output_path = csv_path.parent / "stability_metrics.json"

# --- LOAD JACCARD SCORES ---
avg_jaccards = []

with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            avg_jaccard = float(row["avg_jaccard"])
            avg_jaccards.append(avg_jaccard)
        except ValueError:
            print(f"[WARN] Could not parse row: {row}")

# --- CALCULATE METRICS ---
if avg_jaccards:
    mean_jaccard = round(mean(avg_jaccards), 4)
    median_jaccard = round(median(avg_jaccards), 4)
    percent_perfect = round(
        sum(1 for x in avg_jaccards if x == 1.0) / len(avg_jaccards) * 100, 2
    )

    stability_metrics = {
        "mean_jaccard_similarity": mean_jaccard,
        "median_jaccard_similarity": median_jaccard,
        "output_of_all_runs_identical_percent": percent_perfect,
        "num_elements": len(avg_jaccards)
    }

    # --- SAVE TO JSON ---
    with open(output_path, "w", encoding="utf-8") as jf:
        json.dump(stability_metrics, jf, indent=2)

    print(f"\nStability metrics saved to: {output_path}")

else:
    print("No valid Jaccard scores found in CSV.")
