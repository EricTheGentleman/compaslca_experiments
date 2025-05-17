from methods.material_prompt_builder import build_material_prompt
from methods.material_prompt_builder_ger import build_material_prompt_ger
from methods.utils import load_yaml_config
from pathlib import Path
from openai import OpenAI
import json
import re

# config
material_config_path = Path("configs/00_baseline/material_prompt_config.yaml")
material_config = load_yaml_config(material_config_path)
model_config = material_config.get("model_config", {})
framing_config = material_config.get("prompt_framing_style", {})

# get config values
german_prompt = framing_config.get("german")
key = model_config.get("api_key")
client = OpenAI(api_key='')



# material llm interface
def material_inference(bim_element, material_entries, mode, category):

    # VAR 2: Prompt Language
    if german_prompt == True:
        prompt = build_material_prompt_ger(bim_element, material_entries, mode, category)
    else:
        prompt = build_material_prompt(bim_element, material_entries, mode, category)
        

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