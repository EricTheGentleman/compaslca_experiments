import pandas as pd
import os
import yaml
from pathlib import Path

# === Configuration ===
csv_path = "data/output/category/01_samples_test/category_test_matrix_FFD_res5.csv"
output_dir = Path("configs/category")
output_dir.mkdir(parents=True, exist_ok=True)

# Map CSV column names to YAML keys and structure
yaml_structure = {
    "bim_data_format": {
        "include_geometry": None,  # maps to "geo"
    },
    "prompt_framing_style": {
        "german": None,  # maps to "ger"
    },
    "prompt_reasoning_strategy": {
        "chain_of_thought": None,       # cot
        "extract_then_reason": None,    # etr
        "iterative_self_refinement": None  # isr
    },
    "prompt_contextualization": {
        "include_examples": None  # exp
    }
}

# Order of CSV columns must match variable order for filename
column_to_short = {
    "include_geometry": "geo",
    "german": "ger",
    "chain_of_thought": "cot",
    "extract_then_reason": "etr",
    "iterative_self_refinement": "isr",
    "include_examples": "exp"
}

# Reverse mapping for safe access
short_to_yaml_path = {
    "geo": ("bim_data_format", "include_geometry"),
    "ger": ("prompt_framing_style", "german"),
    "cot": ("prompt_reasoning_strategy", "chain_of_thought"),
    "etr": ("prompt_reasoning_strategy", "extract_then_reason"),
    "isr": ("prompt_reasoning_strategy", "iterative_self_refinement"),
    "exp": ("prompt_contextualization", "include_examples"),
}

# Read CSV
df = pd.read_csv(csv_path)

# Process each row (design run)
for _, row in df.iterrows():
    values = row.drop("Run").astype(int).tolist()
    run_id = row["Run"]

    # Map 0/1 to false/true
    bools = [bool(v) for v in values]

    # Build YAML config
    config = yaml_structure.copy()
    config = {k: v.copy() for k, v in config.items()}  # deep copy

    filename_parts = []

    for short, value in zip(column_to_short.values(), bools):
        section, key = short_to_yaml_path[short]
        config[section][key] = value
        filename_parts.append("t" if value else "f")

    filename = f"{run_id}_{'_'.join(filename_parts)}.yaml"
    filepath = output_dir / filename

    with open(filepath, "w") as f:
        yaml.dump(config, f, sort_keys=False)

    print(f"Created: {filepath}")
