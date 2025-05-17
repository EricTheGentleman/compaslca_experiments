import os
import unicodedata

def get_all_files(base_dir):
    file_set = set()
    for root, _, files in os.walk(base_dir):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), base_dir)
            # Normalize the string for consistent Unicode representation
            normalized = unicodedata.normalize('NFC', rel_path)
            file_set.add(normalized)
    return file_set

def compare_directories(dir1, dir2):
    files_dir1 = get_all_files(dir1)
    files_dir2 = get_all_files(dir2)
    only_in_dir1 = files_dir1 - files_dir2
    only_in_dir2 = files_dir2 - files_dir1
    if only_in_dir1:
        print(f"Files in '{dir1}' but not in '{dir2}':")
        for file in sorted(only_in_dir1):
            print(f"  {os.path.join(dir1, file)}")
    if only_in_dir2:
        print(f"\nFiles in '{dir2}' but not in '{dir1}':")
        for file in sorted(only_in_dir2):
            print(f"  {os.path.join(dir2, file)}")
    if not only_in_dir1 and not only_in_dir2:
        print("Both directories contain the same files.")

# Example usage:
compare_directories("data/input/materials_test/ground_truth", "data/output/material/01_baseline")