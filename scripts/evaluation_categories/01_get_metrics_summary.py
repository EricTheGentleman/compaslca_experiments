import csv
import json
import unicodedata
from pathlib import Path
from statistics import mean

def summarize_category_accuracy(csv_path, output_json_path, parent_dir):
    match_scores = []
    failed_filenames = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        for row in rows:
            match = int(row["match"])
            match_scores.append(match)
            if match == 0:
                failed_filenames.append(row["filename"])

    total_files = len(match_scores)
    success_count = sum(match_scores)
    failure_count = total_files - success_count
    success_ratio = round(success_count / total_files, 4) if total_files else 0.0

    summary = {
        "total_files": total_files,
        "match_summary": {
            "count_success": success_count,
            "count_failure": failure_count,
            "ratio_success": success_ratio,
            "mean_success": round(mean(match_scores), 4) if match_scores else 0.0,
            "failed_filenames": failed_filenames
        },
        "llm_metadata_summary": {}
    }

    # === LLM metadata aggregation ===
    completion_tokens = []
    prompt_tokens = []
    total_tokens = []
    processing_times = []
    inference_costs = []
    companies = set()
    models = set()

    for subdir in ["Elements", "Target_Layers"]:
        subdir_path = Path(parent_dir) / subdir
        if not subdir_path.exists():
            continue

        for json_file in subdir_path.glob("*.json"):
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            metadata = data.get("llm_metadata", {})
            token_usage = metadata.get("token_usage", {})

            completion_tokens.append(token_usage.get("completion_tokens", 0))
            prompt_tokens.append(token_usage.get("prompt_tokens", 0))
            total_tokens.append(token_usage.get("total_tokens", 0))
            processing_times.append(metadata.get("processing_time", 0.0))
            inference_costs.append(metadata.get("inference_cost_usd", 0.0))
            companies.add(metadata.get("company", "unknown"))
            models.add(metadata.get("model", "unknown"))

    def safe_avg(lst):
        return round(mean(lst), 4) if lst else 0.0

    def safe_sum(lst):
        return round(sum(lst), 4) if lst else 0.0

    summary["llm_metadata_summary"] = {
        "total_completion_tokens": safe_sum(completion_tokens),
        "average_completion_tokens": safe_avg(completion_tokens),
        "total_prompt_tokens": safe_sum(prompt_tokens),
        "average_prompt_tokens": safe_avg(prompt_tokens),
        "total_total_tokens": safe_sum(total_tokens),
        "average_total_tokens": safe_avg(total_tokens),
        "total_processing_time_sec": safe_sum(processing_times),
        "average_processing_time_sec": safe_avg(processing_times),
        "total_inference_cost_usd": safe_sum(inference_costs),
        "average_inference_cost_usd": safe_avg(inference_costs),
        "unique_companies": sorted(list(companies)),
        "unique_models": sorted(list(models))
    }

    output_path = Path(output_json_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"Summary written to: {output_path.resolve()}")
# === Example usage ===
if __name__ == "__main__":
    parent_dir = Path("data/output/category/01_baseline")
    input_csv = parent_dir / "metrics_category.csv"
    output_json = parent_dir / "metrics_category_summary.json"

    summarize_category_accuracy(input_csv, output_json, parent_dir)