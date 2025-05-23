import os
import json
import csv

# Directories containing the JSON files
dir1 = "data/input/category_test/ground_truth/Elements"   # <-- Update this
dir2 = "data/input/category_test/ground_truth/Target_Layers"  # <-- Update this

# Output CSV path
output_csv = "data/input/category_test/ground_truth/Samples_Category_Inference.csv"

# Define the column headers and their JSON key mappings
columns = [
    ("name", "Name"),
    ("category", "KBOB Category"),
    ("Type", "Type"),
    ("Matching Scenario", "Matching Scenario"),
    ("Data Structure", "Data Structure"),
    ("Model", "Model"),
    ("Design Stage", "Design Stage"),
    ("Language", "Language"),
    ("Material Entries Count", "Entries Count")
]

# Collect all JSON file paths from both directories
all_files = [
    os.path.join(d, f)
    for d in [dir1, dir2]
    for f in os.listdir(d)
    if f.endswith(".json")
]

# Write to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([col[1] for col in columns])  # Write header

    for filepath in all_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)

            row = [data.get(json_key, "") for json_key, _ in columns]
            writer.writerow(row)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

print(f"CSV export complete: {output_csv}")
