from pathlib import Path

def count_json_files(directory: Path) -> int:
    """Recursively count all .json files in the given directory."""
    return sum(1 for file in directory.rglob("*.json"))


parent_dir = Path("data/output/material/01_baseline")
json_file_count = count_json_files(parent_dir)
print(f"📦 Total JSON files in '{parent_dir}': {json_file_count}")
