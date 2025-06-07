import os
import json
import re

# Constants for cost calculation
COMPLETION_COST_PER_MILLION = 2.40
PROMPT_COST_PER_MILLION = 0.60

# Base path to the runs
base_dir = "data/output/material/01_samples_test/runs"

# Regex to match directories like run_<number>_...
run_pattern = re.compile(r"run_(\d+)_")

# Traverse all directories inside the base runs directory
for run_dir in os.listdir(base_dir):
    match = run_pattern.match(run_dir)
    if match:
        run_number = int(match.group(1))
        if 65 <= run_number <= 128:
            run_path = os.path.join(base_dir, run_dir)
            if os.path.isdir(run_path):
                # Check all subdirectories
                for sub_dir in os.listdir(run_path):
                    sub_dir_path = os.path.join(run_path, sub_dir)
                    if os.path.isdir(sub_dir_path):
                        # Process all JSON files
                        for file_name in os.listdir(sub_dir_path):
                            if file_name.endswith(".json"):
                                file_path = os.path.join(sub_dir_path, file_name)
                                try:
                                    with open(file_path, 'r', encoding='utf-8') as f:
                                        data = json.load(f)

                                    token_usage = data.get("llm_metadata", {}).get("token_usage", {})
                                    completion_tokens = token_usage.get("completion_tokens", 0)
                                    prompt_tokens = token_usage.get("prompt_tokens", 0)

                                    # Compute new inference cost
                                    new_cost = (
                                        completion_tokens * COMPLETION_COST_PER_MILLION / 1_000_000 +
                                        prompt_tokens * PROMPT_COST_PER_MILLION / 1_000_000
                                    )

                                    # Update the field
                                    data["llm_metadata"]["inference_cost_usd"] = round(new_cost, 5)

                                    # Write back the file
                                    with open(file_path, 'w', encoding='utf-8') as f:
                                        json.dump(data, f, indent=2, ensure_ascii=False)

                                    print(f"Updated cost in: {file_path}")

                                except Exception as e:
                                    print(f"Error processing {file_path}: {e}")


