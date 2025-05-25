import yaml
from pathlib import Path
from itertools import product

# === Configuration ===
output_dir = Path("configs/material")
output_dir.mkdir(parents=True, exist_ok=True)

# Order of variables (6 binary factors)
short_vars = ["geo", "ger", "cot", "etr", "isr", "exp"]

# Structure template
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

# Reverse mapping: short -> (section, key)
short_to_yaml_path = {
    "geo": ("bim_data_format", "include_geometry"),
    "ger": ("prompt_framing_style", "german"),
    "cot": ("prompt_reasoning_strategy", "chain_of_thought"),
    "etr": ("prompt_reasoning_strategy", "extract_then_reason"),
    "isr": ("prompt_reasoning_strategy", "iterative_self_refinement"),
    "exp": ("prompt_contextualization", "include_examples"),
}

# Generate all 64 combinations (2^6)
design_matrix = list(product([0, 1], repeat=6))

# Generate YAML for each combination
for i, binary_values in enumerate(design_matrix, start=1):
    bools = [bool(v) for v in binary_values]

    # Build config
    config = {k: v.copy() for k, v in yaml_structure.items()}  # deep copy
    filename_parts = []

    for short, value in zip(short_vars, bools):
        section, key = short_to_yaml_path[short]
        config[section][key] = value
        filename_parts.append("t" if value else "f")

    run_id = f"run_{i}"
    filename = f"{run_id}_{'_'.join(filename_parts)}.yaml"
    filepath = output_dir / filename

    with open(filepath, "w") as f:
        yaml.dump(config, f, sort_keys=False)

    print(f"Created: {filepath}")
