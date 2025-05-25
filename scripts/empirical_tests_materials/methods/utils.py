import yaml
import json
from pathlib import Path


def load_yaml_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def create_inference_folders(input_dir: Path, output_dir: Path):
    if input_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

def get_lci_path_for_category(category: str) -> Path:
    mapping = {
        "Anstrichstoffe, Beschichtungen": Path("data/KBOB/Anstrichstoffe_Beschichtungen/llm_materials.json"), 
        "Beton": Path("data/KBOB/Beton/llm_materials.json"),
        "Bodenbeläge": Path("data/KBOB/Bodenbeläge/llm_materials.json"),
        "Dichtungsbahnen, Schutzfolien": Path("data/KBOB/Dichtungsbahnen_Schutzfolien/llm_materials.json"),
        "Fenster, Sonnenschutz, Fassadenplatten": Path("data/KBOB/Fenster_Sonnenschutz_Fassadenplatten/llm_materials.json"),
        "Holz und Holzwerkstoffe": Path("data/KBOB/Holz_und_Holzwerkstoffe/llm_materials.json"),
        "Kunststoffe": Path("data/KBOB/Kunststoffe/llm_materials.json"),
        "Mauersteine": Path("data/KBOB/Mauersteine/llm_materials.json"),
        "Metallbaustoffe": Path("data/KBOB/Metallbaustoffe/llm_materials.json"),
        "Mörtel und Putze": Path("data/KBOB/Mörtel_und_Putze/llm_materials.json"),
        "Mineralische Platten, Schüttungen, Steine und Ziegel": Path("data/KBOB/Mineralische_Platten_Schüttungen_Steine_und_Ziegel/llm_materials.json"),
        "Türen": Path("data/KBOB/Türen/llm_materials.json"),
        "Wärmedämmstoffe": Path("data/KBOB/Wärmedämmstoffe/llm_materials.json")
    }

    path = mapping.get(category, Path("data/input/LCI_database/KBOB_default"))
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    