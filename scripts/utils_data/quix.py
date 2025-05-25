from pathlib import Path

# === CONFIGURATION ===
parent_dir = Path("data/output/material/01_samples_test/runs")  # Replace with your path

# === Iterate over subdirectories ===
for subfolder in parent_dir.iterdir():
    if subfolder.is_dir():
        # Create Elements and Target_Layers inside each subfolder
        (subfolder / "Elements").mkdir(parents=True, exist_ok=True)
        (subfolder / "Target_Layers").mkdir(parents=True, exist_ok=True)
        print(f"Created in: {subfolder}")
