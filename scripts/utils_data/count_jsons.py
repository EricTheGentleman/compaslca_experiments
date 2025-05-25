from pathlib import Path

# === CONFIGURATION ===
base_dir = Path(r"data/input/materials_test/samples/samples_test/exclude_geometry/Mineralische Platten, Schüttungen, Steine und Ziegel")  # Replace with your target directory

# === Count JSON Files Recursively ===
json_files = list(base_dir.rglob("*.json"))
print(f"Total JSON files found: {len(json_files)}")
