
# This file (and the subsequent prompt configurations) were used for the robustness test of outputs for the material matching prompt
# Recreate runs with with the exact settings (adjust run count directory in lines 57 and 58)


import os
import json
from pathlib import Path
from methods.utils import load_yaml_config, get_lci_path_for_category
from methods.matcher import run_single_match


def match_bim_files(input_dir, output_dir, material_entries, mode_label, category_label, max_input, processed):
    count = 0

    for filename in os.listdir(input_dir):
        if processed + count >= max_input:
            break

        if not filename.endswith(".json"):
            continue

        element_id = os.path.splitext(filename)[0]
        element_path = os.path.join(input_dir, filename)
        result_path = os.path.join(output_dir, f"{element_id}.json")
        os.makedirs(output_dir, exist_ok=True)

        with open(element_path, "r", encoding="utf-8") as f:
            bim_element = json.load(f)

        print(f"> Processing {mode_label.upper()} → {element_id}")

        run_single_match(
            bim_element=bim_element,
            material_entries=material_entries,
            mode=mode_label,
            output_path = result_path,
            category=category_label
        )

        count += 1

    return count



def run_material_inference():
    config_path = Path("configs/00_baseline/material_prompt_config.yaml")
    config = load_yaml_config(config_path)
    var_1_include_geometry = config.get("bim_data_format", {}).get("include_geometry")

    if var_1_include_geometry:
        base_input_dir = Path("data/input/materials_test/samples/stability")
    else:
        base_input_dir = Path("data/input/materials_test/samples/stability")

    output_dir_elements = Path("data/output/material/00_stability/run_10")
    output_dir_layers = Path("data/output/material/00_stability/run_10")
    output_dir_elements.mkdir(parents=True, exist_ok=True)
    output_dir_layers.mkdir(parents=True, exist_ok=True)

    max_input = 50
    processed = 0

    for category_dir in base_input_dir.iterdir():
        if not category_dir.is_dir():
            continue
        if processed >= max_input:
            break

        material_entries = get_lci_path_for_category(category_dir.name)
        input_elements = category_dir / "Elements"
        input_layers = category_dir / "Target_Layers"

        count = match_bim_files(
            input_dir=input_elements,
            output_dir=output_dir_elements,
            material_entries=material_entries,
            mode_label="element",
            category_label=category_dir.name,
            max_input=max_input,
            processed=processed
        )
        processed += count
        if processed >= max_input:
            break

        count = match_bim_files(
            input_dir=input_layers,
            output_dir=output_dir_layers,
            material_entries=material_entries,
            mode_label="layer",
            category_label=category_dir.name,
            max_input=max_input,
            processed=processed
        )
        processed += count
        if processed >= max_input:
            break

if __name__ == "__main__":
    run_material_inference()