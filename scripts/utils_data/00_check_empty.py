import os
import json

# Set the top-level directory to search (change this to your path)
base_dir = "data\input\category_test\ground_truth\gt_test"

# Track files with empty category
empty_category_files = []

# Walk through all subdirectories and files
for root, dirs, files in os.walk(base_dir):
    for filename in files:
        if filename.endswith(".json"):
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("category", "").strip() == "None":
                        empty_category_files.append(file_path)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

# Print results
print(f"Number of JSON files with empty 'category': {len(empty_category_files)}\n")
print("Files with empty 'category':")
for f in empty_category_files:
    print(f)
