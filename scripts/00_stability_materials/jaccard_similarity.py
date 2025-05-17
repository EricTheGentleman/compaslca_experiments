import os
import json
import csv
from pathlib import Path
from itertools import combinations

# ---- Configuration ----
RUN_DIRS = [f"run_{i}" for i in range(1, 11)] 
BASE_PATH = Path("data/output/material/00_stability")
FILE_COUNT = 50

# ---- Jaccard Similarity ----
def jaccard(set1, set2):
    return len(set1 & set2) / len(set1 | set2) if set1 or set2 else 1.0

# ---- Main Logic ----
all_files = os.listdir(BASE_PATH / RUN_DIRS[0])
results = {}

for filename in all_files:
    material_sets = []

    for run_dir in RUN_DIRS:
        filepath = BASE_PATH / run_dir / filename
        if not filepath.exists():
            print(f"[WARN] Missing file: {filepath}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                materials = data["llm_response"]["Matched Materials"]
                material_sets.append(set(materials))
            except Exception as e:
                print(f"[ERROR] Failed to read {filepath}: {e}")
                continue

    # Compute pairwise Jaccard similarities
    similarities = []
    for a, b in combinations(material_sets, 2):
        similarities.append(jaccard(a, b))

    # Store results
    if similarities:
        results[filename] = {
            "avg_jaccard": round(sum(similarities) / len(similarities), 4),
            "min_jaccard": round(min(similarities), 4),
            "max_jaccard": round(max(similarities), 4),
            "num_pairs": len(similarities)
        }

# Write summary to CSV
csv_path = BASE_PATH / "jaccard_summary_materials.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["filename", "avg_jaccard", "min_jaccard", "max_jaccard", "num_pairs"])
    for filename, stats in sorted(results.items()):
        writer.writerow([
            filename,
            stats["avg_jaccard"],
            stats["min_jaccard"],
            stats["max_jaccard"],
            stats["num_pairs"]
        ])
print(f"\nCSV summary saved to: {csv_path}")

