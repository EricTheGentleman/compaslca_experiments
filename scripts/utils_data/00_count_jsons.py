import os

def count_json_files(directory):
    json_count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.json'):
                json_count += 1
    return json_count

if __name__ == "__main__":
    directory_path = "data/input/materials_test/samples/samples_holdout/include_geometry"
    
    total_json_files = count_json_files(directory_path)
    print(f"Total JSON files found: {total_json_files}")