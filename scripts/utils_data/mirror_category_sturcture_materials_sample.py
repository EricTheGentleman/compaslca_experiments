import os
import json
import shutil
from pathlib import Path

def build_category_lookup(ground_truth_dir):
    category_map = {}  # filename -> (category, subdir)

    for category_dir in Path(ground_truth_dir).iterdir():
        if category_dir.is_dir():
            for subdir in ["Elements", "Target_Layers"]:
                sub_path = category_dir / subdir
                if sub_path.exists():
                    for json_file in sub_path.glob("*.json"):
                        category_map[json_file.name] = (category_dir.name, subdir)
    
    return category_map

def organize_discard_geometry(discard_geometry_dir, category_map, output_dir):
    for subdir in ["Elements", "Target_Layers"]:
        source_subdir = Path(discard_geometry_dir) / subdir
        if not source_subdir.exists():
            continue

        for json_file in source_subdir.glob("*.json"):
            filename = json_file.name
            if filename not in category_map:
                print(f"Warning: {filename} not found in ground truth categories. Skipping.")
                continue

            category, correct_subdir = category_map[filename]
            target_dir = Path(output_dir) / category / correct_subdir
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(json_file, target_dir / filename)

# Example usage
ground_truth_dir = "data/input/materials_test/ground_truth_categories"
discard_geometry_dir = "data/input/materials_test/samples/include_geometry"
output_dir = "data/input/materials_test/samples/include_geometry_categories"

category_map = build_category_lookup(ground_truth_dir)
organize_discard_geometry(discard_geometry_dir, category_map, output_dir)
