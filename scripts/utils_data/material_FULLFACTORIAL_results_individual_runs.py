import json
import pandas as pd
from pathlib import Path
from sklearn.metrics import precision_score, recall_score, fbeta_score

# === CONFIGURATION ===
ground_truth_base = Path("data/input/materials_test/ground_truth/gt_holdout")
runs_base = Path("data/output/material/02_samples_holdout/runs")
output_csv_dir = Path("data/output/material/02_samples_holdout/runs_csv")
output_csv_dir.mkdir(parents=True, exist_ok=True)

subfolders = ["Elements", "Target_Layers"]

# === Helper: Compute Scores ===
def compute_scores(gt_materials, predicted_materials):
    gt_set = set(gt_materials)
    pred_set = set(predicted_materials)

    all_materials = list(gt_set.union(pred_set))
    y_true = [1 if m in gt_set else 0 for m in all_materials]
    y_pred = [1 if m in pred_set else 0 for m in all_materials]

    if not any(y_pred) and not any(y_true):
        return 1.0, 1.0, 1.0, 1.0  # All perfect
    elif not any(y_pred):
        return 0.0, 0.0, 0.0, 0.0

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = fbeta_score(y_true, y_pred, beta=1, zero_division=0)
    f05 = fbeta_score(y_true, y_pred, beta=0.5, zero_division=0)

    return precision, recall, f1, f05


# === Load Ground Truth Materials ===
ground_truth = {}  # filename -> list of materials

for subfolder in subfolders:
    gt_path = ground_truth_base / subfolder
    for json_file in gt_path.glob("*.json"):
        try:
            with json_file.open(encoding="utf-8") as f:
                data = json.load(f)
                ground_truth[json_file.name] = data.get("material_entries", [])
        except Exception as e:
            print(f"Error reading GT {json_file}: {e}")

# === Process Each Run Directory ===
for run_dir in runs_base.iterdir():
    if not run_dir.is_dir() or not run_dir.name.startswith("run_"):
        continue

    results = []

    for subfolder in subfolders:
        run_subdir = run_dir / subfolder
        if not run_subdir.exists():
            continue

        for json_file in run_subdir.glob("*.json"):
            gt_materials = ground_truth.get(json_file.name, None)
            if gt_materials is None:
                continue  # No matching ground truth

            try:
                with json_file.open(encoding="utf-8") as f:
                    data = json.load(f)
                    predicted = data.get("llm_response", {}).get("Matched Materials", [])
                    precision, recall, f1, f05 = compute_scores(gt_materials, predicted)

                    results.append({
                        "filename": json_file.name,
                        "precision": precision,
                        "recall": recall,
                        "f1_score": f1,
                        "f0.5_score": f05
                    })

            except Exception as e:
                print(f"Error reading run file {json_file}: {e}")

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Save per-run CSV
    csv_path = output_csv_dir / f"{run_dir.name}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"Saved scores to: {csv_path}")