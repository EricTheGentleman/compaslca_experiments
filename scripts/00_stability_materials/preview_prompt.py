import json
from pathlib import Path
from methods.material_prompt_builder import build_material_prompt
from methods.material_prompt_builder_ger import build_material_prompt_ger

# This is a prompt previewer!

# If you want to preview what the variables do, please adapt them in the config file!

# Specify if you want to include a path for the material entries, or if you want it empty
include_jsons = True

# Specify language
english = False  # False for german

if include_jsons == True:

    # Choose path to JSON files (BIM element & materials list (llm_materials))
    bim_element_path = Path("data/input/materials_test/samples/discard_geometry/Anstrichstoffe, Beschichtungen/Elements/Parkplatz---01-90-PAR_2400-x-5000-10260983.json")
    material_entries_path = Path("data/KBOB/Anstrichstoffe_Beschichtungen/llm_materials.json")
    with open(bim_element_path, "r", encoding="utf-8") as f:
        bim_element = json.load(f)
    with open(material_entries_path, "r", encoding="utf-8") as f:
        material_entries = json.load(f)
else:
    bim_element = "ifc_data"
    material_entries = "material_entries"

# Adjust these variables depending on the input!
mode = "element"  # or "target_layer"
category = "Anstrichstoffe, Beschichtungen"  # gives context-aware example


# === Build the prompt ===

if english == True:
    prompt = build_material_prompt(
        bim_element=bim_element,
        material_entries=material_entries,
        mode=mode,
        category=category
    )
else:
    prompt = build_material_prompt_ger(
        bim_element=bim_element,
        material_entries=material_entries,
        mode=mode,
        category=category
    )   

# === Output the prompt ===

# Print to terminal
print(prompt)

# Optional: Save to file
save_txt = True

if save_txt:
    output_file = Path("data/output/z_preview/preview_output_prompt.txt")
    output_file.write_text(prompt, encoding="utf-8")
    print(f"\nPrompt written to: {output_file.resolve()}")
