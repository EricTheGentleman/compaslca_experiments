from pyDOE2 import ff2n
import os
from pathlib import Path

# === Configuration ===
parent_dir = Path("data/output/category/01_samples_test/runs")  # Change this to your desired parent directory
factor_names = ['A', 'B', 'C', 'D', 'E', 'F']

# Generate fractional factorial design (resolution V) with 6 factors → 32 runs
design_matrix = ff2n(6)[::2]  # Select half (every 2nd row) for 32-run design

# Convert from [-1, 1] to [False, True]
bool_matrix = (design_matrix + 1) / 2  # -1 → 0, 1 → 1

# Create folders
parent_dir.mkdir(parents=True, exist_ok=True)

for i, row in enumerate(bool_matrix, start=1):
    config = '_'.join(['t' if x else 'f' for x in row.astype(int)])
    folder_name = f"run_{i}_{config}"
    folder_path = parent_dir / folder_name
    folder_path.mkdir(exist_ok=True)
    print(f"Created: {folder_path}")
