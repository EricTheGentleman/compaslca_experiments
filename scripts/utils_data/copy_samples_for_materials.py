import os
import shutil

def selective_copy_by_filename(source_dir, reference_dir, destination_dir):
    subdirs = ["Elements", "Target_Layers"]

    for subdir in subdirs:
        source_subdir = os.path.join(source_dir, subdir)
        reference_subdir = os.path.join(reference_dir, subdir)
        destination_subdir = os.path.join(destination_dir, subdir)

        # Ensure destination subdir exists
        os.makedirs(destination_subdir, exist_ok=True)

        # Get filenames in reference directory
        reference_filenames = {
            f for f in os.listdir(reference_subdir) if f.endswith(".json")
        }

        # Copy only matching files
        for filename in reference_filenames:
            source_file_path = os.path.join(source_subdir, filename)
            if os.path.exists(source_file_path):
                shutil.copy(source_file_path, os.path.join(destination_subdir, filename))
            else:
                print(f"File missing in source: {filename}")

# Example usage
directory1 = "data/input/samples_include_geometry"  # Full source
directory2 = "data/input/materials_test/ground_truth"  # Reference for which files to include
directory3 = "data/input/materials_test/samples/include_geometry"  # Destination

selective_copy_by_filename(directory1, directory2, directory3)
print("done!")
