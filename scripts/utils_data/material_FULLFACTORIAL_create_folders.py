from itertools import product
from pathlib import Path

# === Configuration ===
parent_dir = Path("data/output/material/01_samples_test/runs_patch")  # Change as needed
factor_names = ['A', 'B', 'C', 'D', 'E', 'F']

# Generate full factorial design (2^6 = 64 combinations)
design_matrix = list(product([0, 1], repeat=6))  # 0 → False, 1 → True

# Create folders
parent_dir.mkdir(parents=True, exist_ok=True)

for i, row in enumerate(design_matrix, start=1):
    config = '_'.join(['t' if x else 'f' for x in row])
    folder_name = f"run_{i}_{config}"
    folder_path = parent_dir / folder_name
    folder_path.mkdir(exist_ok=True)
    print(f"Created: {folder_path}")
