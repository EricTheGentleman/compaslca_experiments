import os
import shutil
from pathlib import Path

def collect_elements_and_layers(input_base_dir, output_elements_dir, output_layers_dir):
    input_base_dir = Path(input_base_dir)
    output_elements_dir = Path(output_elements_dir)
    output_layers_dir = Path(output_layers_dir)

    output_elements_dir.mkdir(parents=True, exist_ok=True)
    output_layers_dir.mkdir(parents=True, exist_ok=True)

    for subdir in input_base_dir.iterdir():
        if subdir.is_dir():
            elements_dir = subdir / "Elements"
            layers_dir = subdir / "Target_Layers"

            if elements_dir.exists():
                for json_file in elements_dir.glob("*.json"):
                    dest_path = output_elements_dir / json_file.name
                    shutil.copy(json_file, dest_path)

            if layers_dir.exists():
                for json_file in layers_dir.glob("*.json"):
                    dest_path = output_layers_dir / json_file.name
                    shutil.copy(json_file, dest_path)

if __name__ == "__main__":
    collect_elements_and_layers(
        input_base_dir="data/samples/raw_separated",
        output_elements_dir="data/input/Elements",
        output_layers_dir="data/input/Target_Layers"
    )