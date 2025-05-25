from pathlib import Path
import json
from collections import defaultdict

# === CONFIGURATION ===
mismatch_json_dir = Path(r"data/output/category/01_samples_test/runs_mismatches")
summary_output_path = Path(r"data/output/category/01_samples_test/runs_mismatches/mismatch_summary.json")

# === Load All Mismatch JSONs ===
summary = defaultdict(lambda: {
    "category": None,
    "mismatches": defaultdict(int),
    "total_runs_with_mismatch": 0
})

for mismatch_file in mismatch_json_dir.glob("run_*.json"):
    with mismatch_file.open("r", encoding="utf-8") as f:
        mismatches = json.load(f)

    for filename, mismatch_data in mismatches.items():
        gt_category = mismatch_data["category"]
        matched = mismatch_data["matched_category"]

        entry = summary[filename]
        entry["category"] = gt_category  # Should always be the same
        entry["mismatches"][matched] += 1
        entry["total_runs_with_mismatch"] += 1

# === Convert defaultdicts to plain dicts for JSON saving ===
for filename in summary:
    summary[filename]["mismatches"] = dict(summary[filename]["mismatches"])

# === Save Summary JSON ===
with summary_output_path.open("w", encoding="utf-8") as f:
    json.dump(dict(summary), f, indent=2, ensure_ascii=False)

print(f"Summary saved to: {summary_output_path}")
