import json
import textwrap
from methods.utils import load_yaml_config
from methods.material_prompt_components import material_prompt_components
from pathlib import Path

# Get material prompt variables config
material_config_path = Path("configs/00_baseline/material_prompt_config.yaml")
material_config = load_yaml_config(material_config_path)
reasoning_config = material_config.get("prompt_reasoning_strategy", {})
context_config = material_config.get("prompt_contextualization", {})

# get config booleans
cot_bool = reasoning_config.get("chain_of_thought")
etr_bool = reasoning_config.get("extract_then_reason")
isr_bool = reasoning_config.get("iterative_self_refinement")
exp_bool = context_config.get("include_examples")

# assign blocks based on bools
cot = material_prompt_components["chain_of_thought"] if cot_bool else ""
etr = material_prompt_components["extract_then_reason"] if etr_bool else ""
isr = material_prompt_components["iterative_self_refinement"] if isr_bool else ""

# construct dynamic output block
output_format_map = {
    (False, False): material_prompt_components["output_format_baseline"],
    (True,  False): material_prompt_components["output_format_etr"],
    (False, True):  material_prompt_components["output_format_irs"],
    (True,  True):  material_prompt_components["output_format_etr_isr"],
}
output_block = output_format_map.get((etr_bool, isr_bool), material_prompt_components["output_format_baseline"])



# Build dynamic prompt
def build_material_prompt(bim_element, material_entries, mode, category):
    ifc_string = json.dumps(bim_element, indent=2, ensure_ascii=False)
    materials_string = json.dumps(material_entries, indent=2, ensure_ascii=False)

    # Distinguish descriptor of first JSON file
    if mode == "target_layer":
        descriptor_1 = "a **Target Layer** of an IfcBuildingElement"
        descriptor_2 = "'Target Layer of Material Inference'"
    else:
        descriptor_1 = "an **IfcBuildingElement**"
        descriptor_2 = "IfcBuildingElement"

    # Initialize window and concrete specific cases
    concrete_instruct = ""
    window_instruct = ""


    # Load context-aware few-shot examples
    if exp_bool == True:
        if category == "Anstrichstoffe, Beschichtungen":
            exp = material_prompt_components["examples_anstrichstoffe"]
        elif category == "Beton":
            exp = material_prompt_components["examples_beton"]
            concrete_instruct = "- For structural concrete, ignore reinforcement. Just match all viable generic and specifc concretes, and consider the appropriate cement mix for the element type."
        elif category == "Bodenbeläge":
            exp = material_prompt_components["examples_bodenbelaege"]
        elif category == "Dichtungsbahnen, Schutzfolien":
            exp = material_prompt_components["examples_dichtungsbahnen"]
        elif category == "Fenster, Sonnenschutz, Fassadenplatten":
            exp = material_prompt_components["examples_fenster"]
            window_instruct = "- For IfcWindow entities, just match the glazing and don't match the frame options."
        elif category == "Holz und Holzwerkstoffe":
            exp = material_prompt_components["examples_holz"]
        elif category == "Kunststoffe":
            exp = material_prompt_components["examples_kunststoffe"]
        elif category == "Mauersteine":
            exp = material_prompt_components["examples_mauersteine"]
        elif category == "Metallbaustoffe":
            exp = material_prompt_components["examples_metallbaustoffe"]
        elif category == "Mörtel und Putze":
            exp = material_prompt_components["examples_moertel"]
        elif category == "Steine, Schüttungen, Platten und Ziegel":
            exp = material_prompt_components["examples_platten"]
        elif category == "Türen":
            exp = material_prompt_components["examples_tueren"]
        elif category == "Wäremdämmstoffe":
            exp = material_prompt_components["examples_waermedaemstoffe"]
        else:
            exp = ""
    else:
        exp = ""



    # Construct actual prompt
    prompt = textwrap.dedent(f"""\
You are an expert in assigning appropriate materials from a life cycle assessment (LCA) database to BIM elements.
Please complete the following task.

**Material Inference Task**
- You will receive two inputs:
    1. The first input describes {descriptor_1}.
    2. The second input file contains a list of 'Material Options' from an LCA database.
- Identify all 'Material Options' that are **viable matches** for the {descriptor_2} from the first file. 
- Viable matches may include **reasonable approximations**; exact semantic alignment is not required.
- If no viable matches are found, don't assign any materials.
- Base your decision on **all relevant contextual clues** in the first input (e.g., material data, element name, element type, psets).
{cot}
{etr}
{isr}
{output_block}
{exp}
**Input 1 (Data describing {descriptor_2}):**

```json
{ifc_string}
```


**Input 2 (A list containing standardized material options):**

```json
{materials_string}
```
""")
    return prompt