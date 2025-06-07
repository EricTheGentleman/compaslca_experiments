import os
import json
from pathlib import Path
from methods.utils import load_yaml_config, get_lci_path_for_category
from methods.matcher import run_single_match
from methods.preview_prompt import preview_prompt



def match_bim_files(input_dir, output_dir, material_entries, mode_label, category_label, var_config, model_config):
    process_count = 0

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
            var_config = var_config,
            model_config = model_config
        )
    return process_count

def run_material_inference(model_config, var_config, parent_output_path):

    # Get variable for if geometry should be included
    var_1_include_geometry = var_config.get("bim_data_format", {}).get("include_geometry")

    if var_1_include_geometry:
        base_input_dir = Path("data/input/materials_test/samples/samples_test/include_geometry")
    else:
        base_input_dir = Path("data/input/materials_test/samples/samples_test/exclude_geometry")

    # Dynamically create output directories
    output_dir_elements = parent_output_path / "Elements"
    output_dir_layers = parent_output_path / "Target_Layers"
    output_dir_elements.mkdir(parents=True, exist_ok=True)
    output_dir_layers.mkdir(parents=True, exist_ok=True)

    processed = 0

    for category_dir in base_input_dir.iterdir():
        if not category_dir.is_dir():
            continue

        material_entries = get_lci_path_for_category(category_dir.name)
        input_elements = category_dir / "Elements"
        input_layers = category_dir / "Target_Layers"

        processed += match_bim_files(
            input_dir=input_elements,
            output_dir=output_dir_elements,
            material_entries=material_entries,
            mode_label="element",
            category_label=category_dir.name,
            var_config=var_config,
            model_config=model_config
        )

        processed += match_bim_files(
            input_dir=input_layers,
            output_dir=output_dir_layers,
            material_entries=material_entries,
            mode_label="layer",
            category_label=category_dir.name,
            var_config=var_config,
            model_config=model_config
        )



if __name__ == "__main__":
    from pathlib import Path
    from methods.utils import load_yaml_config

    # === Batch Config ===
    var_config_dir = Path("configs/material_test")  # Base dir with all run_*.yaml files
    output_root_dir = Path("data/output/material/01_samples_test_mini/runs")
    model_config_path = Path("configs/model_config.yaml")
    prompts_output_path = Path("data/output/material/01_samples_test_mini/prompts")

    # Load shared model config once
    model_config = load_yaml_config(model_config_path)

    # Iterate over all variable config files
    for var_config_path in sorted(var_config_dir.glob("run_*.yaml")):
        config_name = var_config_path.stem

        print(f"\n=== Running {config_name} ===")

        # Load current var config
        var_config = load_yaml_config(var_config_path)

        # Build output path
        parent_output_path = output_root_dir / config_name
        parent_output_path.mkdir(parents=True, exist_ok=True)

        # Run inference
        run_material_inference(model_config, var_config, parent_output_path)

        # Save prompt preview
        preview_output_path = prompts_output_path / f"prompt_{config_name}.txt"
        preview_prompt(
            var_config=var_config,
            mode="element",
            output_path=preview_output_path
        )