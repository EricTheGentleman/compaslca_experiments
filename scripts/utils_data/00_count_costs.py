import os
import json
import csv

# Define the parent directory containing all run folders
parent_dir = "data/output/material/01_samples_test/runs"
output_csv = "data/output/material/01_samples_test/material_test_costs.csv"

# Prepare list to store results
results = []

# Iterate through each run directory
for run_folder in os.listdir(parent_dir):
    run_path = os.path.join(parent_dir, run_folder)
    if not os.path.isdir(run_path):
        continue

    inference_costs = []
    completion_tokens = []
    prompt_tokens = []

    # Traverse subdirectories for JSON files
    for subdir, _, files in os.walk(run_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(subdir, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        meta = data.get("llm_metadata", {})
                        tokens = meta.get("token_usage", {})

                        # Collect inference cost
                        cost = meta.get("inference_cost_usd", 0)
                        if isinstance(cost, (int, float)):
                            inference_costs.append(cost)

                        # Collect token counts
                        comp = tokens.get("completion_tokens", 0)
                        prompt = tokens.get("prompt_tokens", 0)

                        if isinstance(comp, int):
                            completion_tokens.append(comp)
                        if isinstance(prompt, int):
                            prompt_tokens.append(prompt)

                except (json.JSONDecodeError, FileNotFoundError):
                    print(f"Skipping invalid file: {file_path}")

    num_files = max(len(inference_costs), 1)  # prevent division by zero

    results.append({
        "run_name": run_folder,
        "total_cost": round(sum(inference_costs), 6),
        "average_cost": round(sum(inference_costs) / num_files, 6),
        "total_completion_tokens": sum(completion_tokens),
        "average_completion_tokens": round(sum(completion_tokens) / num_files, 2),
        "total_prompt_tokens": sum(prompt_tokens),
        "average_prompt_tokens": round(sum(prompt_tokens) / num_files, 2)
    })

# Write to CSV
with open(output_csv, 'w', newline='') as csvfile:
    fieldnames = [
        "run_name",
        "total_cost", "average_cost",
        "total_completion_tokens", "average_completion_tokens",
        "total_prompt_tokens", "average_prompt_tokens"
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"Saved summary to {output_csv}")
