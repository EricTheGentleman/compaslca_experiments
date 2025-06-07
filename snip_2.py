import os
import json
from pathlib import Path

# === Configuration ===
first_dir = Path("data/input/category_test/ground_truth/gt_holdout")
second_dir = Path("data/SBE_samples/")
output_json = Path("data/SBE_samples/model_map.json")

# === Subdirectories to check ===
subdirs = ["Elements", "Target_Layers"]

# === Mapping output ===
filename_model_map = {}

# === Process ===
for subdir in subdirs:
    first_sub = first_dir / subdir
    second_sub = second_dir / subdir

    for first_file in first_sub.glob("*.json"):
        second_file = second_sub / first_file.name
        if second_file.exists():
            try:
                with open(first_file, "r") as f:
                    data = json.load(f)
                    model = data.get("Model")
                    if model:
                        filename_model_map[first_file.name] = model
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"Skipping malformed or missing JSON: {first_file}")

# === Save to JSON file ===
output_json.parent.mkdir(parents=True, exist_ok=True)
with open(output_json, "w", encoding="utf-8") as out:
    json.dump(filename_model_map, out, indent=2, ensure_ascii=False)

print(f"Model mapping saved to: {output_json}")
