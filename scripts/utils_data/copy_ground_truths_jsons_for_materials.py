import os
import json
import shutil

def copy_valid_json_files(old_base_dir, new_base_dir):
    subdirs = ["Elements", "Target_Layers"]

    for subdir in subdirs:
        old_dir = os.path.join(old_base_dir, subdir)
        new_dir = os.path.join(new_base_dir, subdir)

        # Ensure the destination directory exists
        os.makedirs(new_dir, exist_ok=True)

        # Loop through JSON files in the original directory
        for filename in os.listdir(old_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(old_dir, filename)

                # Load the JSON and check the "category"
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if data.get("category") != "None":
                        shutil.copy(file_path, os.path.join(new_dir, filename))
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Skipping file due to error: {file_path}\nError: {e}")

# Example usage
old_directory = "data/raw/ground_truth_all"
new_directory = "data/input/materials_test/ground_truth"

copy_valid_json_files(old_directory, new_directory)
