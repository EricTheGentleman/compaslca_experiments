from pathlib import Path

# === CONFIGURATION ===
dir1 = Path("data\input\category_test\ground_truth\gt_test")   # contains 140 JSONs
dir2 = Path("data\output\material/01_samples_test/runs/run_1_f_f_f_f_f_f")  # contains 136 JSONs

# === Collect all JSON filenames recursively ===
files_dir1 = {f.name for f in dir1.rglob("*.json")}
files_dir2 = {f.name for f in dir2.rglob("*.json")}

# === Find missing files ===
missing_files = sorted(files_dir1 - files_dir2)

# === Output ===
print(f"Total in dir1: {len(files_dir1)}")
print(f"Total in dir2: {len(files_dir2)}")
print(f"Missing in dir2: {len(missing_files)}\n")

for fname in missing_files:
    print(fname)
