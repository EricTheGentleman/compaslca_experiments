from methods.material_prompt_builder import build_material_prompt
from methods.material_prompt_builder_ger import build_material_prompt_ger
from openai import OpenAI
import json
import re



# material llm interface
def material_inference(bim_element, material_entries, mode, category, var_config, model_config):

    # Load config (values)
    model_config_temp = model_config.get("model_config", {})
    model_choice = model_config_temp.get("model")
    framing_config = var_config.get("prompt_framing_style", {})
    german = framing_config.get("german")
    key = model_config_temp.get("key")
    client = OpenAI(api_key=key)

    # VAR 2: Prompt Language
    if german:
        prompt = build_material_prompt_ger(bim_element, material_entries, mode, category, var_config)
    else:
        prompt = build_material_prompt(bim_element, material_entries, mode, category, var_config)

    if model_choice in ("gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4.1-nano"):
        # Get LLM response
        response = client.chat.completions.create(
            model=model_choice,
            messages=[{"role": "user", "content": prompt}],
            temperature=model_config_temp.get("temperature"),
            max_tokens=model_config_temp.get("max_tokens")
        )
        # Ensure clean response
        response_text = response.choices[0].message.content
        response_cleaned = re.sub(r"```json|```", "", response_text).strip()
        parsed_response = json.loads(response_cleaned)
               
    token_usage = response.usage
    return parsed_response, token_usage