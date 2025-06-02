import os
import json
from pathlib import Path
from methods.utils import load_yaml_config
from methods.matcher import run_single_match
from methods.preview_prompt import preview_prompt


def match_bim_files(input_dir, output_dir, category_entries, mode_label, var_config, model_config):
    process_count = 0

    for filename in os.listdir(input_dir):

        if not filename.endswith(".json"):
            continue

        process_count +=1

        element_id = os.path.splitext(filename)[0]
        element_path = os.path.join(input_dir, filename)
        result_path = os.path.join(output_dir, f"{element_id}.json")
        os.makedirs(output_dir, exist_ok=True)

        with open(element_path, "r", encoding="utf-8") as f:
            bim_element = json.load(f)

        #print(f"> Processing {mode_label.upper()} → {element_id}")

        run_single_match(
            bim_element=bim_element,
            category_entries=category_entries,
            mode=mode_label,
            output_path = result_path,
            var_config = var_config,
            model_config=model_config
        )

    return process_count


def run_category_inference(model_config, var_config, parent_output_path):

    # Get variable for if geometry should be included
    var_1_include_geometry = var_config.get("bim_data_format", {}).get("include_geometry")

    if var_1_include_geometry:
        base_input_dir = Path("data/input/category_test/samples/samples_holdout/include_geometry")
    else:
        base_input_dir = Path("data/input/category_test/samples/samples_holdout/exclude_geometry")

    # Dynamically create output directories
    output_dir_elements = parent_output_path / "Elements"
    output_dir_layers = parent_output_path / "Target_Layers"
    output_dir_elements.mkdir(parents=True, exist_ok=True)
    output_dir_layers.mkdir(parents=True, exist_ok=True)

    processed = 0

    with open(Path("data/KBOB/llm_categories.json"), "r", encoding="utf-8") as f:
        category_entries = json.load(f)
    input_elements = base_input_dir / "Elements"
    input_layers = base_input_dir / "Target_Layers"

    processed += match_bim_files(
        input_dir=input_elements,
        output_dir=output_dir_elements,
        category_entries=category_entries,
        mode_label="element",
        var_config = var_config,
        model_config=model_config
    )

    processed += match_bim_files(
        input_dir=input_layers,
        output_dir=output_dir_layers,
        category_entries=category_entries,
        mode_label="layer",
        var_config = var_config,
        model_config=model_config
    )
    
    print(f"\n Inference completed. Inference count: {processed}")




if __name__ == "__main__":
    from pathlib import Path
    from methods.utils import load_yaml_config

    # === Batch Config ===
    var_config_dir = Path("configs/category_holdout_2")  # Base dir with all run_*.yaml files
    output_root_dir = Path("data/output/category/02_samples_holdout/runs")
    model_config_path = Path("configs/model_config.yaml")
    prompts_output_path = Path("data/output/category/02_samples_holdout/prompts")

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
        run_category_inference(model_config, var_config, parent_output_path)

        # Save prompt preview
        preview_output_path = prompts_output_path / f"prompt_{config_name}.txt"
        preview_prompt(
            var_config=var_config,
            mode="element",
            output_path=preview_output_path
        )
