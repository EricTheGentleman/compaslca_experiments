import csv
import json
from pathlib import Path
from statistics import mean, variance, stdev

import csv
import json
from pathlib import Path
from statistics import mean, variance, stdev

def summarize_metrics_from_csv(csv_path, output_json_path, parent_dir):
    metrics = {
        "jaccard_index": [],
        "precision": [],
        "recall": [],
        "f1_score": [],
        "f0.5_score": []
    }

    success_f1_flags = []
    success_f05_flags = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        for row in rows:
            for metric in metrics:
                value = float(row[metric])
                metrics[metric].append(value)

            if "success_f1" in row:
                success_f1_flags.append(int(row["success_f1"]))
            if "success_f05" in row:
                success_f05_flags.append(int(row["success_f05"]))

    total_files = len(rows)

    def compute_success_summary(flags):
        num_success = sum(flags)
        num_failures = len(flags) - num_success
        return {
            "count_success": num_success,
            "count_failure": num_failures,
            "ratio_success": round(num_success / len(flags), 4) if flags else 0.0,
            "ratio_failure": round(num_failures / len(flags), 4) if flags else 0.0,
            "mean_success": round(mean(flags), 4) if flags else 0.0
        }

    summary = {
        "total_files": total_files,
        "metrics": {},
        "success_f1_summary": compute_success_summary(success_f1_flags),
        "success_f05_summary": compute_success_summary(success_f05_flags),
        "llm_metadata_summary": {}
    }

    for metric, values in metrics.items():
        summary["metrics"][metric] = {
            "mean": round(mean(values), 4),
            "variance": round(variance(values), 6) if len(values) > 1 else 0.0,
            "std_dev": round(stdev(values), 4) if len(values) > 1 else 0.0,
            "min": round(min(values), 4),
            "max": round(max(values), 4),
            "count_perfect": sum(1 for v in values if v == 1.0),
            "count_zero": sum(1 for v in values if v == 0.0),
            "count": len(values)
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

    # Write summary to JSON
    output_path = Path(output_json_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Summary written to: {output_path.resolve()}")


# === Example usage ===
if __name__ == "__main__":
    parent_dir = Path("data/output/material/02_combinations/t_t_t_t_t_t")
    input_csv = parent_dir / "metrics_all.csv"
    output_json = parent_dir / "metrics_summary.json"

    summarize_metrics_from_csv(input_csv, output_json, parent_dir)