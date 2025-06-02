from pathlib import Path
import json

# === CONFIGURATION ===
ground_truth_base = Path(r"data/input/category_test/ground_truth/gt_holdout")
runs_base = Path(r"data/output/category/02_samples_holdout/runs")
output_json_dir = Path(r"data/output/category/02_samples_holdout/runs_mismatches")  # Target directory for JSON outputs
output_json_dir.mkdir(parents=True, exist_ok=True)

subfolders = ["Elements", "Target_Layers"]

# === Load Ground Truth Categories ===
ground_truth = {}

for subfolder in subfolders:
    gt_path = ground_truth_base / subfolder
    for json_file in gt_path.glob("*.json"):
        with json_file.open(encoding="utf-8") as f:
            data = json.load(f)
            ground_truth[json_file.name] = data.get("category", "")

# === Process Each Run ===
for run_dir in runs_base.iterdir():
    if not run_dir.is_dir() or not run_dir.name.startswith("run_"):
        continue

    mismatches = {}

    for subfolder in subfolders:
        run_subdir = run_dir / subfolder
        if not run_subdir.exists():
            continue

        for json_file in run_subdir.glob("*.json"):
            filename = json_file.name
            gt_category = ground_truth.get(filename, None)
            if gt_category is None:
                continue

            try:
                with json_file.open(encoding="utf-8") as f:
                    data = json.load(f)
                    matched_category = data.get("llm_response", {}).get("Matched Category", "")
                    if matched_category.strip() != gt_category.strip():
                        mismatches[filename] = {
                            "category": gt_category,
                            "matched_category": matched_category
                        }
            except Exception as e:
                print(f"Error reading {json_file}: {e}")

    # Save mismatches as JSON
    json_output_path = output_json_dir / f"{run_dir.name}.json"
    with json_output_path.open("w", encoding="utf-8") as f:
        json.dump(mismatches, f, indent=2, ensure_ascii=False)

    print(f"Saved mismatches: {json_output_path}")
