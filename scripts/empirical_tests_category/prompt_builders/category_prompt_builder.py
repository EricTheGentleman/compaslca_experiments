from category_prompt_components import category_prompt_components as components
from utils import load_yaml_config

# Load config
config = load_yaml_config("path/to/config.yaml")

# Get the configs for the category prompt
# Assemble string "blocks" to easily append to baseline prompt
def get_category_prompt_blocks(config):

    # Access subsection from YAML config
    framing = config.get("prompt_framing_style", {})
    reasoning = config.get("prompt_reasoning_strategy", {})
    context = config.get("prompt_contextualization", {})

    # Family 3: Framing
    framing_blocks = []
    if framing.get("expert_role_emphasis"):
        framing_blocks.append(components["expert_role_emphasis"])
    if framing.get("content_framing") == "assertive":
        framing_blocks.append(components["content_framing"])
    if framing.get("analysis_granularity") == "efficient":
        framing_blocks.append(components["analysis_granularity_efficient"])
    elif framing.get("analysis_granularity") == "thorough":
        framing_blocks.append(components["analysis_granularity_thorough"])

    # Family 4: Reasoning
    reasoning_blocks = []
    if reasoning.get("chain_of_thought"):
        reasoning_blocks.append(components["chain_of_thought"])
    if reasoning.get("iterative_self_refinement"):
        reasoning_blocks.append(components["iterative_self_refinement"])
    if reasoning.get("summarize_first"):
        reasoning_blocks.append(components["summarize_first"])

    # Family 5: Context
    emphasis = context.get("data_emphasis", "none")
    emphasis_key_map = {
        "metadata": "data_emphasis_meta",
        "material": "data_emphasis_mat",
        "geometry": "data_emphasis_geom",
        "psets": "data_emphasis_pset"
    }
    emphasis_block = components.get(emphasis_key_map.get(emphasis, ""), "")

    # Output blocks

    # === Scenario Explanation
    scenario_block = components["scenario_explanation"] if context.get("scenario_explanation") else ""

    # === Decision Justification
    if framing.get("decision_justification"):
        justification_text = components["decision_justification"]
        justification_json = components["decision_justification_json"]
        comma = ","
    else:
        justification_text = ""
        justification_json = ""
        comma = ""

    return {
        "framing_block": "\n".join(framing_blocks),
        "reasoning_block": "\n".join(reasoning_blocks),
        "emphasis_block": emphasis_block,
        "scenario_block": scenario_block,
        "justification_text": justification_text,
        "justification_json": justification_json,
        "comma": comma,
    }


def build_category_prompt(bim_element, category_data, mode):
    pass





config = load_yaml_config("config/master_config.yaml")
blocks = get_category_prompt_blocks(config)

# prompt = build_category_prompt(bim_element, category_data, blocks, mode)