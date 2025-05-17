import json
import csv
from pathlib import Path

# === Define your configs here ===
# Format: "directory_path": [config_name, param1, param2, ..., param6]
CONFIGS = {
    "data/output/material/00_pilot_data/f_f_f_f_f_f": ["config_1", 0, 0, 0, 0, 0, 0],
    "data/output/material/00_pilot_data/f_t_f_t_f_t": ["config_2", 0, 1, 0, 1, 0, 1],
    "data/output/material/00_pilot_data/t_f_t_f_t_f": ["config_3", 1, 0, 1, 0, 1, 0],
    "data/output/material/00_pilot_data/t_t_t_t_t_t": ["config_4", 1, 1, 1, 1, 1, 1]
}

OUTPUT_CSV = "data/output/material/00_pilot_data/pilot_data.csv"
TRIALS = 191  # Fixed number for all rows

def extract_metrics(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    f1_success = data.get("success_f1_summary", {}).get("count_success", 0)
    f05_success = data.get("success_f05_summary", {}).get("count_success", 0)
    return f1_success, f05_success

def create_summary_csv(configs, output_csv, trials):
    rows = []

    for path_str, config_data in configs.items():
        config_path = Path(path_str) / "metrics_summary.json"
        config_name = config_data[0]
        booleans = config_data[1:]

        if not config_path.exists():
            print(f"Missing: {config_path}")
            continue

        f1_success, f05_success = extract_metrics(config_path)

        row = {
            "config_name": config_name,
            "geo": booleans[0],
            "ger": booleans[1],
            "cot": booleans[2],
            "etr": booleans[3],
            "isr": booleans[4],
            "exp": booleans[5],
            "f1_success": f1_success,
            "f0.5_success": f05_success,
            "trials": trials
        }
        rows.append(row)

    # Write CSV
    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Summary CSV written to: {Path(output_csv).resolve()}")

# === Run ===
if __name__ == "__main__":
    create_summary_csv(CONFIGS, OUTPUT_CSV, TRIALS)
