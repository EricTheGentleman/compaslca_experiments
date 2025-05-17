from methods.prompt_builders import build_category_prompt, build_material_prompt
from methods.utils import load_yaml_config
from pathlib import Path
from openai import OpenAI
import json
import re

# === Category Inference ===

# config
config_path = Path("configs/00_baseline/category_prompt_config.yaml")
category_config = load_yaml_config(config_path)
config = category_config.get("model_parameters", {})
cat_key = config.get("api_key")
cat_client = OpenAI(api_key=cat_key)

# category llm interface
def category_inference(bim_element, category_data, mode):
    prompt = build_category_prompt(bim_element, category_data, mode)
    response = cat_client.chat.completions.create(
        model=config.get("model"),
        messages=[{"role": "user", "content": prompt}],
        temperature=config.get("temperature"),
        max_tokens=config.get("max_tokens")
    )
    response_text = response.choices[0].message.content
    response_cleaned = re.sub(r"```json|```", "", response_text).strip()
    parsed_response = json.loads(response_cleaned)
    token_usage = response.usage
    return parsed_response, token_usage