# This is a prompt previewer!

# If you want to preview what the variables do, please adapt them in the config file!

from pathlib import Path
from methods.utils import load_yaml_config
from methods.category_prompt_builder import build_category_prompt
from methods.category_prompt_builder_ger import build_category_prompt_ger

def preview_prompt(
    var_config,
    mode="element",  # or "target_layer"
    output_path="data/output/z_preview/preview_output_prompt.txt"
):
    # Load language setting from config
    framing_config = var_config.get("prompt_framing_style", {})
    german = framing_config.get("german", True)

    # Set dummy
    bim_element = "IFC Data of Iterated Element / Target Layer"
    category_entries = "List of Material Entries of the Inferred Category"

    # Build the prompt
    if german:
        prompt = build_category_prompt_ger(
            bim_element=bim_element,
            category_entries=category_entries,
            mode=mode,
            var_config = var_config
        )
    else:
        prompt = build_category_prompt(
            bim_element=bim_element,
            category_entries=category_entries,
            mode=mode,
            var_config = var_config
        )

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(prompt, encoding="utf-8")
