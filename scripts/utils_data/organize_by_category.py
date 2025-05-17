import os
import json
import shutil
from pathlib import Path

def organize_by_category(source_dir, output_base_dir):
    subdirs = ["Elements", "Target_Layers"]

    for subdir in subdirs:
        source_subdir = Path(source_dir) / subdir

        for json_file in source_subdir.glob("*.json"):
            try:
                with open(json_file, encoding="utf-8") as f:
                    data = json.load(f)

                category = data.get("category")
                if not category:
                    continue  # Skip if category is missing or None

                # Create category directory with Elements and Target_Layers inside
                category_dir = Path(output_base_dir) / category
                target_subdir = category_dir / subdir
                target_subdir.mkdir(parents=True, exist_ok=True)

                # Copy the file to the appropriate location
                shutil.copy(json_file, target_subdir / json_file.name)

            except (json.JSONDecodeError, IOError) as e:
                print(f"Error processing {json_file}: {e}")

# Example usage
source_directory = "data/input/materials_test/ground_truth"
output_directory = "data/input/materials_test/ground_truth_categories"

organize_by_category(source_directory, output_directory)
