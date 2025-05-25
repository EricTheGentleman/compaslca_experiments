from pathlib import Path
import shutil

# === CONFIGURATION ===
first_parent = Path("data/output/material/01_samples_test/runs")
second_parent = Path("data/output/material/01_samples_test/runs_patch")

# === Iterate through all subdirectories and their sub-subdirs in second_parent
for subdir in second_parent.iterdir():
    if not subdir.is_dir():
        continue

    for subsub in ["Elements", "Target_Layers"]:
        second_subsub_path = subdir / subsub
        if not second_subsub_path.exists():
            continue

        for json_file in second_subsub_path.glob("*.json"):
            # Compute corresponding path in the first parent directory
            relative_path = json_file.relative_to(second_parent)
            first_json_path = first_parent / relative_path

            if first_json_path.exists():
                shutil.copy(json_file, first_json_path)
                print(f"Overwritten: {first_json_path}")
            else:
                print(f"Skipped (not found in first parent): {first_json_path}")
