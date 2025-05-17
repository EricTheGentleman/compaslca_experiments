import os
import json

# Set your input and output directories here
input_dir = "data/samples/raw_unseparated/LTU"
output_dir = "data/samples/raw_unseparated/LTU_Fixed"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Constants for scaling
VOLUME_SCALE = 1e-9
AREA_SCALE = 1e-6

for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        try:
            # Detect format
            if "Element Geometry Data" in data:
                geo_data = data["Element Geometry Data"]
            elif "Building Element Context" in data and "Element Geometry Data" in data["Building Element Context"]:
                geo_data = data["Building Element Context"]["Element Geometry Data"]
            else:
                raise KeyError("Element Geometry Data not found")

            compas_data = geo_data["Quantities (COMPAS)"]
            old_volume = compas_data["Net Volume"]
            old_area = compas_data["Entire Surface Area"]
            bbox_volume = geo_data["Bounding Box Volume"]

            # Scale values
            new_volume = round(old_volume * VOLUME_SCALE, 5)
            new_area = round(old_area * AREA_SCALE, 5)
            new_ratio = new_volume / bbox_volume if bbox_volume != 0 else None

            # Apply changes
            compas_data["Net Volume"] = new_volume
            compas_data["Entire Surface Area"] = new_area
            geo_data["Real Volume to Bounding Box Volume Ratio"] = round(new_ratio, 5)

            # Save result
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

        except KeyError as e:
            print(f"Skipping {filename}: missing key {e}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
