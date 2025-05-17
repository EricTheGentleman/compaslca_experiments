import os
import shutil
import re
from pathlib import Path

def allocate_json_files(input_base_dir, output_base_dir):
    input_base_dir = Path(input_base_dir)
    output_base_dir = Path(output_base_dir)

    layer_pattern = re.compile(r"_L([1-9][0-9]?|100)\.json$")

    for subdir in input_base_dir.iterdir():
        if subdir.is_dir():
            # Set up new subdirectory structure
            new_elements_dir = output_base_dir / subdir.name / "Elements"
            new_layers_dir = output_base_dir / subdir.name / "Target_Layers"
            new_elements_dir.mkdir(parents=True, exist_ok=True)
            new_layers_dir.mkdir(parents=True, exist_ok=True)

            # Process each JSON file in the current subdir
            for file in subdir.glob("*.json"):
                destination_dir = (
                    new_layers_dir if layer_pattern.search(file.name)
                    else new_elements_dir
                )
                shutil.copy(file, destination_dir / file.name)

if __name__ == "__main__":
    allocate_json_files(
        input_base_dir="data/raw/ground_truth_unseparated",
        output_base_dir="data/raw/ground_truth_separated"
    )
