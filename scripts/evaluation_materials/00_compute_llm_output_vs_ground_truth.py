import json
import csv
from pathlib import Path

def load_materials_from_ground_truth(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return set(data.get("material_entries", [])), data.get("category", "unknown")

def load_materials_from_baseline(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return set(data.get("llm_response", {}).get("Matched Materials", []))

def compute_metrics(gt_set, pred_set):
    intersection = gt_set & pred_set
    union = gt_set | pred_set

    jaccard = len(intersection) / len(union) if union else 1.0
    precision = len(intersection) / len(pred_set) if pred_set else (1.0 if not gt_set else 0.0)
    recall = len(intersection) / len(gt_set) if gt_set else (1.0 if not pred_set else 0.0)
    
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    beta = 0.5
    f05 = (1 + beta**2) * precision * recall / ((beta**2 * precision) + recall) if (precision + recall) else 0.0

    return round(jaccard, 3), round(precision, 3), round(recall, 3), round(f1, 3), round(f05, 3)

def evaluate_material_matches(ground_truth_dir, baseline_dir, output_csv):
    rows = []

    for mode in ["Elements", "Target_Layers"]:
        gt_mode_dir = ground_truth_dir / mode
        bl_mode_dir = baseline_dir / mode
        if not gt_mode_dir.exists() or not bl_mode_dir.exists():
            print("   ⏭️  Skipping — one of the folders doesn't exist.")
            continue

        for gt_file in gt_mode_dir.glob("*.json"):
            bl_file = bl_mode_dir / gt_file.name
            if not bl_file.exists():
                print(f"Missing in baseline: {bl_file.name}")
                continue

            gt_materials, _ = load_materials_from_ground_truth(gt_file)
            bl_materials = load_materials_from_baseline(bl_file)

            jaccard, precision, recall, f1, f05 = compute_metrics(gt_materials, bl_materials)
            success_f1 = 1 if f1 >= 0.7 else 0
            success_f05 = 1 if f05 >= 0.7 else 0

            rows.append({
                "filename": gt_file.name,
                "mode": mode,
                "jaccard_index": jaccard,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "f0.5_score": f05,
                "success_f1": success_f1,
                "success_f05": success_f05
            })

    if not rows:
        print("No matching JSON file pairs found. Nothing to write.")
        return

    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nEvaluation complete. CSV written to: {output_path.resolve()}")

# === Example usage ===
if __name__ == "__main__":
    ground_truth_dir = Path("data/input/materials_test/ground_truth")
    run_dir = Path("data/output/material/02_combinations/t_t_t_t_t_t")
    output_csv = "data/output/material/02_combinations/t_t_t_t_t_t/metrics_all.csv"

    evaluate_material_matches(ground_truth_dir, run_dir, output_csv)
