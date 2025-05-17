# This is a prompt previewer!

# If you want to preview what the variables do, please adapt them in the config file!

from pathlib import Path
from methods.utils import load_yaml_config
from methods.material_prompt_builder import build_material_prompt
from methods.material_prompt_builder_ger import build_material_prompt_ger

def preview_prompt(
    config,
    mode="element",  # or "target_layer"
    category="Beton",
    output_path="data/output/z_preview/preview_output_prompt.txt"
):
    # Load language setting from config
    framing_config = config.get("prompt_framing_style", {})
    german = framing_config.get("german", True)

    # Set dummy
    bim_element = "IFC Data of Iterated Element / Target Layer"
    material_entries = "List of Material Entries of the Inferred Category"

    # Build the prompt
    if german:
        prompt = build_material_prompt_ger(
            bim_element=bim_element,
            material_entries=material_entries,
            mode=mode,
            category=category,
            config = config
        )
    else:
        prompt = build_material_prompt(
            bim_element=bim_element,
            material_entries=material_entries,
            mode=mode,
            category=category,
            config = config
        )

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(prompt, encoding="utf-8")
