import pandas as pd
import unicodedata

# Load both CSV files
df_file = pd.read_csv('data/output/material/02_samples_holdout/runs_csv/claude_opus_4.csv')  # CSV with 'filename' column
df_name = pd.read_csv('data/input/materials_test/ground_truth/Samples_Holdout.csv')      # CSV with 'Name' column

# Function to normalize Unicode and remove '.json'
def clean_filename(value):
    value = unicodedata.normalize('NFC', value)  # Normalize Unicode
    value = value.strip().replace('.json', '')
    return value

# Clean both columns for matching
df_file['match_key'] = df_file['filename'].apply(clean_filename)
df_name['match_key'] = df_name['Name'].apply(lambda x: unicodedata.normalize('NFC', x.strip()))

# Merge on the cleaned match_key
merged_df = pd.merge(df_name, df_file, on='match_key', how='left', suffixes=('_name', '_file'))

# Drop match_key if not needed
merged_df.drop(columns=['match_key'], inplace=True)

# Save the merged result
output_path = "data/output/material/03_feature_analysis/02_holdout_set.csv"
merged_df.to_csv(output_path, index=False)

print("Merged CSV saved as 'merged_result.csv'")
