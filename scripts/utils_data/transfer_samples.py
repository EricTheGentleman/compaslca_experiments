import pandas as pd
import os
import shutil
from pathlib import Path

# === Configuration ===
csv_path = "data/input/category_test/ground_truth/Samples_Holdout.csv"  # path to your CSV file
source_dir = Path("data/input/category_test/samples/samples_all/include_geometry")  # parent directory with Elements and Target_Layers
target_dir = Path("data/input/category_test/samples/samples_holdout/include_geometry")  # parent directory where Elements and Target_Layers will be copied to

# Load CSV and extract names
df = pd.read_csv(csv_path)
names_to_copy = set(df["Name"].astype(str))

# Subdirectories to handle
subdirs = ["Elements", "Target_Layers"]

# Process each subdirectory
for subdir in subdirs:
    src_subdir = source_dir / subdir
    dst_subdir = target_dir / subdir
    dst_subdir.mkdir(parents=True, exist_ok=True)

    for name in names_to_copy:
        json_filename = f"{name}.json"
        src_file = src_subdir / json_filename
        dst_file = dst_subdir / json_filename

        if src_file.exists():
            shutil.copy2(src_file, dst_file)
        else:
            pass
