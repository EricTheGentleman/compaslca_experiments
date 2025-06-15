import json
import pandas as pd
from pathlib import Path
from sklearn.metrics import precision_score, recall_score, fbeta_score
from unicodedata import normalize

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
ground_truth = {}
for subfolder in subfolders:
    gt_path = ground_truth_base / subfolder
    for json_file in gt_path.glob("*.json"):
        try:
            with json_file.open(encoding="utf-8") as f:
                data = json.load(f)
                norm_name = normalize("NFC", json_file.name)
                ground_truth[norm_name] = data.get("material_entries", [])
        except Exception as e:
            print(f"Error reading GT {json_file}: {e}")

# === Process Each Run Directory ===
for run_dir in runs_base.iterdir():
    if not run_dir.is_dir():
        continue  # Skip non-directories

    results = []

    for subfolder in subfolders:
        run_subdir = run_dir / subfolder
        if not run_subdir.exists():
            continue

        for json_file in run_subdir.glob("*.json"):
            norm_name = normalize("NFC", json_file.name)
            gt_materials = ground_truth.get(norm_name)
            if gt_materials is None:
                print(f"⚠️ GT not found for: {json_file.name}")
                continue

            try:
                with json_file.open(encoding="utf-8") as f:
                    data = json.load(f)
                    llm_response = data.get("llm_response", {})
                    llm_metadata = data.get("llm_metadata", {})

                    matched_materials = llm_response.get("Matched Materials", [])
                    precision, recall, f1, f05 = compute_scores(gt_materials, matched_materials)

                    # Extract metadata
                    entries_count = len(matched_materials)
                    cost = llm_metadata.get("inference_cost_usd", 0.0)
                    proc_time = llm_metadata.get("processing_time", 0.0)

                    results.append({
                        "filename": json_file.name,
                        "precision": precision,
                        "recall": recall,
                        "f1_score": f1,
                        "f0.5_score": f05,
                        "Entries Count": entries_count,
                        "Cost": cost,
                        "Processing Time": proc_time
                    })

            except Exception as e:
                print(f"Error reading run file {json_file}: {e}")

    # Convert results to DataFrame and save
    df = pd.DataFrame(results)
    csv_path = output_csv_dir / f"{run_dir.name}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"✅ Saved per-sample scores to: {csv_path}")
