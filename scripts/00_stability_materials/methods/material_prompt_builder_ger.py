import json
import textwrap
from methods.utils import load_yaml_config
from methods.material_prompt_components_ger import material_prompt_components_ger
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
cot = material_prompt_components_ger["chain_of_thought"] if cot_bool else ""
etr = material_prompt_components_ger["extract_then_reason"] if etr_bool else ""
isr = material_prompt_components_ger["iterative_self_refinement"] if isr_bool else ""

# construct dynamic output block
output_format_map = {
    (False, False): material_prompt_components_ger["output_format_baseline"],
    (True,  False): material_prompt_components_ger["output_format_etr"],
    (False, True):  material_prompt_components_ger["output_format_irs"],
    (True,  True):  material_prompt_components_ger["output_format_etr_isr"],
}
output_block = output_format_map.get((etr_bool, isr_bool), material_prompt_components_ger["output_format_baseline"])



# Build dynamic prompt
def build_material_prompt_ger(bim_element, material_entries, mode, category):
    ifc_string = json.dumps(bim_element, indent=2, ensure_ascii=False)
    materials_string = json.dumps(material_entries, indent=2, ensure_ascii=False)

    # Distinguish descriptor of first JSON file
    if mode == "target_layer":
        descriptor_1 = "ein **Target Layer** von einem IfcBuildingElement"
        descriptor_2 = "die 'Target Layer of Material Inference'"
    else:
        descriptor_1 = "ein **IfcBuildingElement**"
        descriptor_2 = "das IfcBuildingElement"

    # Load context-aware few-shot examples
    if exp_bool == True:
        if category == "Anstrichstoffe, Beschichtungen":
            exp = material_prompt_components_ger["examples_anstrichstoffe"]
        elif category == "Beton":
            exp = material_prompt_components_ger["examples_beton"]
        elif category == "Bodenbeläge":
            exp = material_prompt_components_ger["examples_bodenbelaege"]
        elif category == "Dichtungsbahnen, Schutzfolien":
            exp = material_prompt_components_ger["examples_dichtungsbahnen"]
        elif category == "Fenster, Sonnenschutz, Fassadenplatten":
            exp = material_prompt_components_ger["examples_fenster"]
        elif category == "Holz und Holzwerkstoffe":
            exp = material_prompt_components_ger["examples_holz"]
        elif category == "Kunststoffe":
            exp = material_prompt_components_ger["examples_kunststoffe"]
        elif category == "Mauersteine":
            exp = material_prompt_components_ger["examples_mauersteine"]
        elif category == "Metallbaustoffe":
            exp = material_prompt_components_ger["examples_metallbaustoffe"]
        elif category == "Mörtel und Putze":
            exp = material_prompt_components_ger["examples_moertel"]
        elif category == "Steine, Schüttungen, Platten und Ziegel":
            exp = material_prompt_components_ger["examples_platten"]
        elif category == "Türen":
            exp = material_prompt_components_ger["examples_tueren"]
        elif category == "Wäremdämmstoffe":
            exp = material_prompt_components_ger["examples_waermedaemstoffe"]
        else:
            exp = ""
    else:
        exp = ""



    # Construct actual prompt
    prompt = textwrap.dedent(f"""\
Du bist ein Experte darin, geeignete Materialien aus einer Ökobilanz (LCA) Datenbank Bauelementen im IFC-Modell zuzuordnen
Bitte führe die folgende Aufgabe aus:

**Aufgabe zur Materialzuordnung**
- Du erhälst zwei Eingaben:
    1. Die erste Eingabe beschreibt {descriptor_1}.
    2. Die zweite Eingabe enthält eine Liste von "material_options" aus einer LCA-Datenbank.
- Identifiziere alle "material_options", die **geeignete Entsprechungen** für {descriptor_2} aus der ersten Eingabe darstellen. 
- Geeignete Entsprechungen können **plausible Annäherungen** einschließen; eine exakte semantische Übereinstimmung ist nicht erforderlich.
- Falls keine geeigneten Entsprechungen gefunden werden, ordne keine Materialien zu.
- Stütze deine Entscheidung auf **alle relevanten Kontextinformationen** aus der ersten Eingabe (z.B. material data, element name, element type, psets).
{cot}
{etr}
{isr}
{output_block}
{exp}
**Eingabe 1 (Daten, welche {descriptor_2} beschreiben):**

```json
{ifc_string}
```


**Eingabe 2 (Eine Liste mit standardisierten Materialoptionen):**

```json
{materials_string}
```
""")
    return prompt