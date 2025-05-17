import os
import json
from pathlib import Path
from methods.utils import load_yaml_config, get_lci_path_for_category
from methods.matcher import run_single_match
from methods.preview_prompt import preview_prompt


def match_bim_files(input_dir, output_dir, material_entries, mode_label, category_label, config):

    for filename in os.listdir(input_dir):

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
            category=category_label,
            config = config
        )


def run_material_inference(config, parent_output_path):

    # Get variable for if geometry should be included
    var_1_include_geometry = config.get("bim_data_format", {}).get("include_geometry")

    if var_1_include_geometry:
        #base_input_dir = Path("data/input/materials_test/samples/discard_geometry")
        base_input_dir = Path("data/input/materials_test/samples_test")
    else:
        #base_input_dir = Path("data/input/materials_test/samples/include_geometry")
        base_input_dir = Path("data/input/materials_test/samples_test")

    # Dynamically create output directories
    output_dir_elements = parent_output_path / "Elements"
    output_dir_layers = parent_output_path / "Target_Layers"
    output_dir_elements.mkdir(parents=True, exist_ok=True)
    output_dir_layers.mkdir(parents=True, exist_ok=True)

    for category_dir in base_input_dir.iterdir():
        if not category_dir.is_dir():
            continue

        material_entries = get_lci_path_for_category(category_dir.name)
        input_elements = category_dir / "Elements"
        input_layers = category_dir / "Target_Layers"

        match_bim_files(
            input_dir=input_elements,
            output_dir=output_dir_elements,
            material_entries=material_entries,
            mode_label="element",
            category_label=category_dir.name,
            config = config
        )

        match_bim_files(
            input_dir=input_layers,
            output_dir=output_dir_layers,
            material_entries=material_entries,
            mode_label="layer",
            category_label=category_dir.name,
            config = config
        )

if __name__ == "__main__":

    # Specify parent output dir
    # parent_output_path = Path("data/output/material/01_baseline")
    parent_output_path = Path("data/output/material/01_baseline_test")

    # Specify config path
    config_path = Path("configs/00_baseline/material_prompt_config.yaml")
    config = load_yaml_config(config_path)

    # Run inference(s) and return prompt preview
    run_material_inference(config, parent_output_path)

    # Specify preview params
    mode = "element"
    category = "Beton" # only relevant if context_aware example is toggled to true
    preview_output_path = parent_output_path / "prompt.txt"

    preview_prompt(
        config=config,
        mode=mode,
        category=category,
        output_path=preview_output_path
    )