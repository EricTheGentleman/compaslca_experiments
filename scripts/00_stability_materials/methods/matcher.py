import json
import time
from methods.llm_interface import material_inference
from methods.utils import load_yaml_config
from pathlib import Path

# config
material_config_path = Path("configs/00_baseline/material_prompt_config.yaml")
material_config = load_yaml_config(material_config_path)
model_config = material_config.get("model_config", {})
company = model_config.get("company")
model = model_config.get("model")

# Performs material match for a BIM element and writes the result to disk.
def run_single_match(bim_element, material_entries, output_path, mode, category):
    start_time = time.time()
    llm_response, token_usage = material_inference(bim_element, material_entries, mode, category)
    end_time = time.time()
    processing_time = round(end_time - start_time, 3)

    matched_name = llm_response.get("Matched Material Name")
    if matched_name in [None, "None", "", []]:
        matched_name = None

    # Token usage
    token_data = token_usage.to_dict()
    prompt_tokens = token_data.get("prompt_tokens", 0)
    completion_tokens = token_data.get("completion_tokens", 0)

    # Cost calculation (gpt 4o - May 2025)
    cost_per_1k_prompt = 0.005      # $5.00 / 1M input tokens
    cost_per_1k_completion = 0.02   # $20.00 / 1M output tokens
    total_cost = round(
        (prompt_tokens * cost_per_1k_prompt / 1000) +
        (completion_tokens * cost_per_1k_completion / 1000), 6
    )

    metadata = {
        "matched_type": "material",
        "category": category,
        "message": "Match successful" if matched_name else "No match found",
        "token_usage": token_usage.to_dict(),
        "processing_time": processing_time,
        "company": company,
        "model": model,
        "inference_cost_usd": total_cost
    }

    result = {
        "llm_response": llm_response,
        "llm_metadata": metadata
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result
