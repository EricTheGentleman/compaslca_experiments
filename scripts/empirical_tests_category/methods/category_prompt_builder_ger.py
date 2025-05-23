import json
from methods.category_prompt_components_ger import category_prompt_components_ger

# Build dynamic prompt
def build_category_prompt_ger(bim_element, category_entries, mode, config):

    # Load the inputs of the current element as strings
    ifc_string = json.dumps(bim_element, indent=2, ensure_ascii=False)
    # Corresponding material entries list
    categories_string = json.dumps(category_entries, indent=2, ensure_ascii=False)

    # Get config values
    reasoning_config = config.get("prompt_reasoning_strategy", {})
    context_config = config.get("prompt_contextualization", {})

    # get config booleans
    cot_bool = reasoning_config.get("chain_of_thought")
    etr_bool = reasoning_config.get("extract_then_reason")
    isr_bool = reasoning_config.get("iterative_self_refinement")
    exp_bool = context_config.get("include_examples")

    # assign blocks based on bools
    cot = category_prompt_components_ger["chain_of_thought"] if cot_bool else ""
    etr = category_prompt_components_ger["extract_then_reason"] if etr_bool else ""
    isr = category_prompt_components_ger["iterative_self_refinement"] if isr_bool else ""

    # construct dynamic output block
    output_format_map = {
        (False, False): category_prompt_components_ger["output_format_baseline"],
        (True,  False): category_prompt_components_ger["output_format_etr"],
        (False, True):  category_prompt_components_ger["output_format_irs"],
        (True,  True):  category_prompt_components_ger["output_format_etr_isr"],
    }
    output_block = output_format_map.get((etr_bool, isr_bool), category_prompt_components_ger["output_format_baseline"])

    # Distinguish descriptor of first JSON file
    if mode == "target_layer":
        descriptor_1 = "ein **Target Layer** von einem IfcBuildingElement"
        descriptor_2 = "die 'Target Layer of Material Inference'"
    else:
        descriptor_1 = "ein **IfcBuildingElement**"
        descriptor_2 = "das IfcBuildingElement"


    # Load few-shot examples
    exp = ""
    if exp_bool == True:
        exp = category_prompt_components_ger["examples"]


    # Construct static lines
    static_lines_1 = [
        "Du bist ein Experte darin, BIM-Elemente in Kategorien einer Lebenszyklusanalyse (LCA) Datanbank einzuordnen.",
        "Bitte führe die folgende Aufgabe aus.",
        "",
        "**Aufgabe zur Kategoriezuordnung**",
        "- Du erhälst zwei Eingaben:",
        f"  1. Die erste Eingabe beschreibt {descriptor_1}.",
        "  2. Die zweite Eingabe beschreibt eine Liste von Kategorien von einer LCA Datenbank.",
        f"- Identifiziere die genaueste Kategorie für {descriptor_2} aus der ersten Datei.",
        "- Generell gilt: Wenn ein Materialname verfügbar ist, dann priorisiere die Kategoriezuordnung basierend auf dem Materialnamen.",
        f"- Du musst eine Kategorie auswählen, bei der du passende Materialeinträge für {descriptor_2} erwartest.",
        "- Wenn kein Materialname vorhanden ist, dann basiere deine Entscheidungen auf **allen anderen relevanten Kontextinformationen** aus der ersten Eingabe (z.B. Elementname, Elementtyp, Psets)."
    ]

    # Include optional blocks (with dynamic spacing)
    dynamic_lines = [
        cot,
        etr,
        isr,
        output_block,
        exp,
    ]
    dynamic_lines = [line for line in dynamic_lines if line.strip()]

    # Construct static lines
    static_lines_2 = [
        f"**Eingabe 1 (Daten, welche {descriptor_2} beschreibt):**",
        "",
        "```json",
        ifc_string,
        "```",
        "",
        "**Eingabe 2 (Eine Liste mit Kategorien einer LCA Datenbank):**",
        "",
        "```json",
        categories_string,
        "```"
    ]

    # Combine lines (this is the only way to control dynamic spacing)
    lines = static_lines_1 + dynamic_lines + static_lines_2

    # Construct actual prompt
    prompt = "\n".join(lines)
    return prompt