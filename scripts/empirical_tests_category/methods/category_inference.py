import os
import json
import time
from methods.utils import load_json
from methods.llm_interface import category_inference, material_inference

def infer_category(bim_element, current_dir, results_dir, mode):
    category_file = os.path.join(current_dir, "llm_categories.json")
    index_file = os.path.join(current_dir, "index.json")

    if not os.path.exists(index_file):
        raise FileNotFoundError(f"Missing index.json in {current_dir}")
    if not os.path.exists(category_file):
        raise FileNotFoundError(f"Missing llm_categories.json in {current_dir}")

    index_data = load_json(index_file)
    lci_data = load_json(category_file)

    # Run category inference
    start_time = time.time()
    llm_response, token_usage = category_inference(bim_element, lci_data, mode)
    end_time = time.time()
    processing_time = round(end_time - start_time, 3)

    category_name = llm_response.get("Matched Material Category")
    if category_name in [None, "None", "", []]:
        category_name = None

    # Metadata
    metadata = {
        "matched_type": "category",
        "matched_path": str(current_dir),
        "message": "Match successful" if category_name else "No match found",
        "token_usage": token_usage.to_dict(),
        "processing_time": processing_time
    }

    result = {
        "llm_response": llm_response,
        "llm_metadata": metadata
    }

    result_path = os.path.join(results_dir, "category_inference_result.json")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result