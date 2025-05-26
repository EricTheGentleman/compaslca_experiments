import json
import pandas as pd
from pathlib import Path
from sklearn.metrics import precision_score, recall_score, fbeta_score
import unicodedata


# === CONFIGURATION ===
ground_truth_base = Path("data/input/category_test/ground_truth/gt_test")
runs_base = Path("data/output/material/01_samples_test/runs")
output_csv_dir = Path("data/output/pipeline/01_samples_test/runs_csv")
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
                filename_normalized = unicodedata.normalize("NFC", json_file.name)
                ground_truth[filename_normalized] = data.get("material_entries", [])
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
            filename_normalized = unicodedata.normalize("NFC", json_file.name)
            gt_materials = ground_truth.get(filename_normalized, None)
            if gt_materials is None:
                continue

            try:
                with json_file.open(encoding="utf-8") as f:
                    data = json.load(f)
                    predicted = data.get("llm_response", {}).get("Matched Materials", [])
                    precision, recall, f1, f05 = compute_scores(gt_materials, predicted)

                    results.append({
                        "Name": filename_normalized.removesuffix(".json"),
                        "precision": precision,
                        "recall": recall,
                        "f1_score": f1,
                        "f0.5_score": f05
                    })

            except Exception as e:
                print(f"Error reading run file {json_file}: {e}")

    # === Step: Create DataFrame from results ===
    df = pd.DataFrame(results)

    # === Step: Mark all rows as Category Passed TRUE by default ===
    df["Category Passed"] = "TRUE"

    # === Step: Set default FALSE for known category failures that were skipped in step 1 ===
    true_negatives_in_category_inference = {
        unicodedata.normalize("NFC", s) for s in {
            "1072_210525_TreppeInnenRevitExport_MK-1072_210525_TreppeInnenRevitExport_MK-7935324",
            "Stair-Residential---200mm-Max-Riser-250mm-Tread-151086-1",
            "Surface-2872326",
            "hlks1-hlks-10122938"
        }
    }

    # Set default for new column
    df["True Negative Cat. Inference"] = "FALSE"

    # Remove the known skipped files
    df = df[~df["Name"].isin(true_negatives_in_category_inference)]

    # Re-add them with perfect scores and "TRUE" in both columns
    df = pd.concat([
        df,
        pd.DataFrame([{
            "Name": fname,
            "precision": 1.0,
            "recall": 1.0,
            "f1_score": 1.0,
            "f0.5_score": 1.0,
            "Category Passed": "TRUE",
            "True Negative Cat. Inference": "TRUE"
        } for fname in true_negatives_in_category_inference])
    ], ignore_index=True)

    # === Step: Retroactively downgrade scores for known processed failures ===
    category_failed_but_processed = {
        unicodedata.normalize("NFC", s) for s in {
            "Basic-Wall-WAN_ASW_MW_225-7610934",
            "Basic-Wall-WAN_TWÄ_MW_125---EI30-11161798",
            "Basic-Wall-Exterior---Brick-on-Block-138062_L6",
            "Floor-Finish-Floor---Ceramic-Tile-169772_L1"
        }
    }

    # Set scores and flag to FALSE for those
    df.loc[df["Name"].isin(category_failed_but_processed), [
        "precision", "recall", "f1_score", "f0.5_score"
    ]] = 0.0
    df.loc[df["Name"].isin(category_failed_but_processed), "Category Passed"] = "FALSE"

    # Save per-run CSV
    csv_path = output_csv_dir / f"{run_dir.name}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"Saved scores to: {csv_path}")
