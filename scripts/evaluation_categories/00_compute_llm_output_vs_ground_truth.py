import json
import csv
from pathlib import Path

def load_category_from_ground_truth(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("category", "None")

def load_category_from_llm_output(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("llm_response", {}).get("Matched Category", "None")

def evaluate_category_matches(ground_truth_dir, llm_output_dir, output_csv):
    results = []

    for mode in ["Elements", "Target_Layers"]:
        gt_mode_dir = ground_truth_dir / mode
        llm_mode_dir = llm_output_dir / mode

        if not gt_mode_dir.exists() or not llm_mode_dir.exists():
            print(f"⚠️ Skipping {mode} — one of the folders does not exist.")
            continue

        for gt_file in gt_mode_dir.glob("*.json"):
            llm_file = llm_mode_dir / gt_file.name
            if not llm_file.exists():
                print(f"⚠️ Missing LLM output for: {gt_file.name}")
                continue

            gt_category = load_category_from_ground_truth(gt_file)
            llm_category = load_category_from_llm_output(llm_file)

            match = int(gt_category == llm_category)

            results.append({
                "filename": gt_file.name,
                "mode": mode,
                "ground_truth": gt_category,
                "llm_prediction": llm_category,
                "match": match
            })

    if not results:
        print("❌ No results to write.")
        return

    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Evaluation complete. Results written to: {output_path.resolve()}")

# === Example usage ===
if __name__ == "__main__":
    ground_truth_dir = Path("data/input/category_test/ground_truth")
    llm_output_dir = Path("data/output/category/01_baseline")
    output_csv = "data/output/category/01_baseline/metrics_category.csv"

    evaluate_category_matches(ground_truth_dir, llm_output_dir, output_csv)
