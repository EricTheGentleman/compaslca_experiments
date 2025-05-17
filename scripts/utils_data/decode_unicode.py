import os
import json

def decode_unicode(directory, recursive=False):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)

                except Exception as e:
                    pass
        if not recursive:
            break 

top_level = "data/samples/raw_unseparated"

for subfolder in os.listdir(top_level):
    subfolder_path = os.path.join(top_level, subfolder)
    if os.path.isdir(subfolder_path):
        decode_unicode(subfolder_path, recursive=False)