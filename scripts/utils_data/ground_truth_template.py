import os
import json
from pathlib import Path

source_root = Path("data/samples/raw")
target_root = Path("data/samples/ground_truth")

target_root.mkdir(parents=True, exist_ok=True)

for subdir, _, files in os.walk(source_root):
    subdir_path = Path(subdir)
    relative_subdir = subdir_path.relative_to(source_root)
    target_subdir = target_root / relative_subdir
    target_subdir.mkdir(parents=True, exist_ok=True)

    for file in files:
        if file.endswith(".json"):
            filename_without_ext = Path(file).stem
            new_data = {
                "name": filename_without_ext,
                "category": "",
                "material_entries": [],
                "reason": []
            }

            target_file_path = target_subdir / f"{filename_without_ext}.json"

            with open(target_file_path, "w", encoding="utf-8") as f:
                json.dump(new_data, f, indent=4, ensure_ascii=False)
