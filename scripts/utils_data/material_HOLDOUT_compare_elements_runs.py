import os
import pandas as pd
import re
import unicodedata

def extract_run_number(col_name):
    match = re.match(r"run_(\d+)(_|$)", col_name)
    return int(match.group(1)) if match else float('inf')


# === Configuration ===
input_dir = "data/output/material/02_samples_holdout/runs_csv"
output_file = "data/output/material/02_samples_holdout/material_holdout_f0.5_matrix.csv"
reference_csv = "data/input/materials_test/ground_truth/Samples_Holdout.csv"
score = "f0.5_score"

# === Step 1: Read and prepare reference metadata ===
reference_df = pd.read_csv(reference_csv, encoding='utf-8')

# Normalize the Name column to fix umlaut inconsistencies
reference_df["Name"] = reference_df["Name"].apply(lambda x: unicodedata.normalize("NFC", str(x)))

# === Step 2: Read and collect all run CSVs ===
all_runs = {}

for file in os.listdir(input_dir):
    if file.endswith(".csv"):
        run_name = file[:-4]  # Strip '.csv'
        file_path = os.path.join(input_dir, file)
        
        df = pd.read_csv(file_path)
        df["Name"] = df["filename"].str.replace(".json", "", regex=False)
        
        # Normalize Name column here as well
        df["Name"] = df["Name"].apply(lambda x: unicodedata.normalize("NFC", str(x)))
        
        run_df = df[["Name", score]].copy()
        run_df = run_df.rename(columns={score: run_name})
        
        all_runs[run_name] = run_df

# === Step 3: Merge all run DataFrames on 'Name' ===
merged_df = None
for run_df in all_runs.values():
    if merged_df is None:
        merged_df = run_df
    else:
        merged_df = pd.merge(merged_df, run_df, on="Name", how="outer")

# Sort by Name
merged_df = merged_df.sort_values(by="Name")

# Reorder columns: 'Name' first, then run columns sorted numerically
cols = merged_df.columns.tolist()
run_cols = sorted([col for col in cols if col != "Name"], key=extract_run_number)
merged_df = merged_df[["Name"] + run_cols]

# === Step 4: Calculate mean of run scores ===
merged_df["mean"] = merged_df[run_cols].mean(axis=1)

# === Step 5: Merge with reference metadata ===
final_df = pd.merge(merged_df, reference_df, on="Name", how="left")

# === Step 6: Reorder columns: Name + Metadata + Runs + Mean ===
metadata_cols = [
    "KBOB Category", "Type", "Matching Scenario", "Data Structure",
    "Model", "Design Stage", "Language", "Entries Count"
]

# Make sure all metadata columns exist (avoids KeyErrors if some are missing)
metadata_cols = [col for col in metadata_cols if col in final_df.columns]

# Move columns into desired order
final_df = final_df[["Name"] + metadata_cols + run_cols + ["mean"]]

# === Step 7: Save to CSV with BOM for Excel compatibility ===
final_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"Combined CSV with metadata saved to: {output_file}")