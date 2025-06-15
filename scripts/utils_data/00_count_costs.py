import os
import json

# Set your parent directory here
parent_dir = "data/output/category/02_samples_holdout/runs/openai_o3_pro"  # ⬅️ change this to your actual path

# set costs:
input_tokens = 20  # per 1M tokens
output_tokens = 80  # per 1M tokens


updated_files = 0
skipped_files = []

for root, _, files in os.walk(parent_dir):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                metadata = data.get("llm_metadata", {})
                token_usage = metadata.get("token_usage", {})
                prompt_tokens = token_usage.get("prompt_tokens", 0)
                completion_tokens = token_usage.get("completion_tokens", 0)

                # Calculate the new inference cost
                cost = (prompt_tokens * input_tokens + completion_tokens * output_tokens) / 1_000_000

                # Overwrite the field
                metadata["inference_cost_usd"] = round(cost, 10)  # round for clean output

                # Save back to file
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                updated_files += 1

            except Exception as e:
                skipped_files.append((file_path, str(e)))

# Summary output
print(f"✅ Updated inference_cost_usd in {updated_files} JSON files.")
if skipped_files:
    print(f"⚠️ Skipped {len(skipped_files)} files due to errors:")
    for path, msg in skipped_files:
        print(f"  {path}: {msg}")

