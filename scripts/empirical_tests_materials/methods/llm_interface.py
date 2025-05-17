from methods.material_prompt_builder import build_material_prompt
from methods.material_prompt_builder_ger import build_material_prompt_ger
from openai import OpenAI
import json
import re



# material llm interface
def material_inference(bim_element, material_entries, mode, category, config):

    # Load config (values)
    model_config = config.get("model_config", {})
    framing_config = config.get("prompt_framing_style", {})
    german = framing_config.get("german")
    key = model_config.get("key")
    client = OpenAI(api_key=key)

    # VAR 2: Prompt Language
    if german:
        prompt = build_material_prompt_ger(bim_element, material_entries, mode, category, config)
    else:
        prompt = build_material_prompt(bim_element, material_entries, mode, category, config)

    # Get LLM response
    response = client.chat.completions.create(
        model=model_config.get("model"),
        messages=[{"role": "user", "content": prompt}],
        temperature=model_config.get("temperature"),
        max_tokens=model_config.get("max_tokens")
    )

    # Ensure clean response
    response_text = response.choices[0].message.content
    response_cleaned = re.sub(r"```json|```", "", response_text).strip()
    parsed_response = json.loads(response_cleaned)
    token_usage = response.usage
    return parsed_response, token_usage