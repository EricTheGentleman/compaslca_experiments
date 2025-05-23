import json
from methods.category_prompt_components import category_prompt_components

# Build dynamic prompt
def build_category_prompt(bim_element, category_entries, mode, config):

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
    cot = category_prompt_components["chain_of_thought"] if cot_bool else ""
    etr = category_prompt_components["extract_then_reason"] if etr_bool else ""
    isr = category_prompt_components["iterative_self_refinement"] if isr_bool else ""

    # construct dynamic output block
    output_format_map = {
        (False, False): category_prompt_components["output_format_baseline"],
        (True,  False): category_prompt_components["output_format_etr"],
        (False, True):  category_prompt_components["output_format_irs"],
        (True,  True):  category_prompt_components["output_format_etr_isr"],
    }
    output_block = output_format_map.get((etr_bool, isr_bool), category_prompt_components["output_format_baseline"])

    # Distinguish descriptor of first JSON file
    if mode == "target_layer":
        descriptor_1 = "a **Target Layer** of an IfcBuildingElement"
        descriptor_2 = "'Target Layer of Material Inference'"
    else:
        descriptor_1 = "an **IfcBuildingElement**"
        descriptor_2 = "IfcBuildingElement"


    # Load few-shot examples
    exp = ""
    if exp_bool == True:
        exp = category_prompt_components["examples"]


    # Construct static lines
    static_lines_1 = [
        "You are an expert in classifying BIM elements to life cycle assessment (LCA) categories.",
        "Please complete the following task.",
        "",
        "**Category Inference Task**",
        "- You will receive two inputs:",
        f"  1. The first input describes {descriptor_1}.",
        "  2. The second input file contains a list of 'Categories' from an LCA database.",
        f"- Identify the most accurate category for the {descriptor_2} from the first file.",
        "- In general, if a material name is available, then prioritize matching the category based on the material name, rather than something else.",
        f"- You must match a category where you anticipate finding viable material entries for the {descriptor_2}.",
        f"- If the {descriptor_2} cannot be clearly classified, assign an empty list.",
        "- If there is no material name, base your decision on **all other relevant contextual clues** in the first input (e.g., element name, element type, psets)."
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
        f"**Input 1 (Data describing {descriptor_2}):**",
        "",
        "```json",
        ifc_string,
        "```",
        "",
        "**Input 2 (A list containing categories for an LCA database):**",
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