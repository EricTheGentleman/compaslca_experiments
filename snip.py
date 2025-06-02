import json
from pathlib import Path

# 🔧 Set your parent directory here
PARENT_DIR = Path("data/input/category_test/ground_truth/gt_test")

# Stores counts and matched names per subdir
results = {}

# Traverse subdirectories
for subdir in PARENT_DIR.iterdir():
    if subdir.is_dir():
        hilo_count = 0
        total = 0
        hilo_names = []

        for json_file in subdir.rglob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    total += 1
                    if data.get("Model") == "HiLo":
                        hilo_count += 1
                        name = data.get("name", "<no name>")
                        hilo_names.append(name)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Skipping {json_file} – error: {e}")

        results[subdir.name] = {
            "total_jsons": total,
            "hilo_count": hilo_count,
            "hilo_names": hilo_names
        }

# ✅ Print summary
print("\n=== 'Model': 'HiLo' Counts Per Subdirectory ===")
for name, stats in sorted(results.items()):
    print(f"{name}: {stats['hilo_count']} of {stats['total_jsons']} JSONs")

print("\n=== Names of JSONs with 'Model': 'HiLo' ===")
for dir_name, stats in sorted(results.items()):
    if stats["hilo_names"]:
        print(f"\n{dir_name}:")
        for entry in stats["hilo_names"]:
            print(f"  - {entry}")
