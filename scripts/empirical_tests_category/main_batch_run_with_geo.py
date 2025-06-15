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
        base_input_dir = Path("data/input/category_test/samples/samples_test/include_geometry")
    else:
        base_input_dir = Path("data/input/category_test/samples/samples_test/exclude_geometry")

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

    # === Fixed variable config dir ===
    var_config_dir = Path("configs/category_test_geo")

    # === Define model config paths and their corresponding outputs ===
    model_configs = {
        "4o-mini": {
            "model_config_path": Path("configs/category_test_models/model_config_4o-mini.yaml"),
            "output_root_dir": Path("data/output/category/01_samples_test_4o-mini/runs"),
            "prompts_output_path": Path("data/output/category/01_samples_test_4o-mini/prompts"),
        },
        "4o": {
            "model_config_path": Path("configs/category_test_models/model_config_4o.yaml"),
            "output_root_dir": Path("data/output/category/01_samples_test_4o/runs"),
            "prompts_output_path": Path("data/output/category/01_samples_test_4o/prompts"),
        }
    }

    # === Loop over each model config
    for model_name, paths in model_configs.items():
        model_config_path = paths["model_config_path"]
        output_root_dir = paths["output_root_dir"]
        prompts_output_path = paths["prompts_output_path"]

        # Load model config
        model_config = load_yaml_config(model_config_path)

        # Loop over all variable configs
        for var_config_path in sorted(var_config_dir.glob("run_*.yaml")):
            config_name = var_config_path.stem

            print(f"\n=== Running {config_name} with model {model_name} ===")

            var_config = load_yaml_config(var_config_path)

            parent_output_path = output_root_dir / config_name
            parent_output_path.mkdir(parents=True, exist_ok=True)

            run_category_inference(model_config, var_config, parent_output_path)

            preview_output_path = prompts_output_path / f"prompt_{config_name}.txt"
            preview_prompt(
                var_config=var_config,
                mode="element",
                output_path=preview_output_path
            )
