import ast
import os

import ast
import re

def clean_python_list_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract variable name and list using regex
    match = re.match(r"\s*(\w+)\s*=\s*(\[.*\])", content, re.DOTALL)
    if not match:
        raise ValueError("Could not parse variable assignment or list.")

    var_name, list_text = match.groups()

    try:
        data = ast.literal_eval(list_text)
        if not isinstance(data, list):
            raise ValueError("The file does not contain a list.")
    except Exception as e:
        raise ValueError(f"Invalid list format: {e}")

    # Deduplicate and sort
    cleaned = sorted(set(data), key=str.casefold)

    # Write it back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"{var_name} = [\n")
        for item in cleaned:
            f.write(f'    "{item}",\n')
        f.write("]\n")

    print(f"✅ Cleaned and updated: {file_path}")


clean_python_list_file("configs/templates/pset_selection.py")
