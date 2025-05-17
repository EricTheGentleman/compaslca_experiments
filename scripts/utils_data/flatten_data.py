import os
import shutil
from pathlib import Path

def flatten_elements_and_target_layers(input_root, output_root):
    input_root = Path(input_root)
    output_elements_dir = Path(output_root) / "Elements"
    output_target_layers_dir = Path(output_root) / "Target_Layers"

    output_elements_dir.mkdir(parents=True, exist_ok=True)
    output_target_layers_dir.mkdir(parents=True, exist_ok=True)

    for dirpath, dirnames, filenames in os.walk(input_root):
        path = Path(dirpath)
        if path.name == "Elements":
            for filename in filenames:
                if filename.endswith(".json"):
                    src = path / filename
                    dst = output_elements_dir / f"{path.parent.name}_{filename}"
                    shutil.copy2(src, dst)
        elif path.name == "Target_Layers":
            for filename in filenames:
                if filename.endswith(".json"):
                    src = path / filename
                    dst = output_target_layers_dir / f"{path.parent.name}_{filename}"
                    shutil.copy2(src, dst)

def flatten(input_root, output_root):
    input_root = Path(input_root)
    output_elements_dir = Path(output_root) / "Elements"
    output_target_layers_dir = Path(output_root) / "Target_Layers"

    output_elements_dir.mkdir(parents=True, exist_ok=True)
    output_target_layers_dir.mkdir(parents=True, exist_ok=True)

    for dirpath, dirnames, filenames in os.walk(input_root):
        path = Path(dirpath)
        if path.name == "Elements":
            for filename in filenames:
                if filename.endswith(".json"):
                    src = path / filename
                    dst = output_elements_dir / f"{filename}"
                    shutil.copy2(src, dst)
        elif path.name == "Target_Layers":
            for filename in filenames:
                if filename.endswith(".json"):
                    src = path / filename
                    dst = output_target_layers_dir / f"{filename}"
                    shutil.copy2(src, dst)


flatten(
    input_root="data/raw/ground_truth_separated",
    output_root="data/raw/ground_truth_all"
)

"""
flatten_elements_and_target_layers(
    input_root="data/raw/samples_separated",
    output_root="data/raw/samples_all_model_name"
)
"""