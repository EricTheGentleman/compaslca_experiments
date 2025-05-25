from pathlib import Path
import json
import shutil

# === CONFIGURATION ===
gt_base = Path(r"data/input/category_test/ground_truth/gt_holdout")
samples_base = Path(r"data/input/category_test/samples/samples_holdout/exclude_geometry")
output_base = Path(r"data/input/materials_test/samples/samples_holdout/exclude_geometry")

# Create output base directory if it doesn't exist
output_base.mkdir(parents=True, exist_ok=True)

subfolders = ["Elements", "Target_Layers"]

# === Step 1: Collect all unique categories ===
category_map = {}  # filename -> category

unique_categories = set()

for subfolder in subfolders:
    gt_dir = gt_base / subfolder
    for json_file in gt_dir.glob("*.json"):
        try:
            with json_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                category = data.get("category", "").strip()
                if category:
                    category_map[json_file.name] = category
                    unique_categories.add(category)
        except Exception as e:
            print(f"Error reading {json_file}: {e}")

# === Step 2: Create output directory structure ===
for category in unique_categories:
    cat_dir = output_base / category
    (cat_dir / "Elements").mkdir(parents=True, exist_ok=True)
    (cat_dir / "Target_Layers").mkdir(parents=True, exist_ok=True)

# === Step 3: Copy sample files based on category ===
for subfolder in subfolders:
    sample_dir = samples_base / subfolder
    for sample_file in sample_dir.glob("*.json"):
        category = category_map.get(sample_file.name)
        if not category:
            continue  # Skip if no matching category from ground truth

        destination = output_base / category / subfolder / sample_file.name
        try:
            shutil.copy(sample_file, destination)
        except Exception as e:
            print(f"Error copying {sample_file} to {destination}: {e}")

print("✅ All files organized by category.")
