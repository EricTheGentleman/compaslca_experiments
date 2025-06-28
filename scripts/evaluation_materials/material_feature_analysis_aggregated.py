import pandas as pd
import json

# Load the two input CSV files
df1 = pd.read_csv('data/output/material/03_feature_analysis/01_development_set.csv')
df2 = pd.read_csv('data/output/material/03_feature_analysis/02_holdout_set.csv')

# Combine both DataFrames
combined_df = pd.concat([df1, df2], ignore_index=True)

# Group by 'Type' and compute the average f0.5_score and sample count
summary_df = combined_df.groupby('Matching Scenario').agg(
    **{
        'Average F0.5 Score': ('f0.5_score', 'mean'),
        'Number of Samples': ('f0.5_score', 'count')
    }
).reset_index()

# Save the summary CSV
output_path_csv = 'data/output/material/03_feature_analysis/material_matchscenario_feature.csv'
summary_df.to_csv(output_path_csv, index=False)
print(f"Summary saved to {output_path_csv}")

# Create a dictionary with Type as keys and unique names as list values
type_name_mapping = combined_df.groupby('Matching Scenario')['Name'].unique().apply(list).to_dict()

# Save the mapping to a JSON file
output_path_json = 'data/output/material/03_feature_analysis/material_matchscenario_names.json'
with open(output_path_json, 'w', encoding='utf-8') as f:
    json.dump(type_name_mapping, f, indent=4, ensure_ascii=False)
print(f"Name mapping saved to {output_path_json}")
