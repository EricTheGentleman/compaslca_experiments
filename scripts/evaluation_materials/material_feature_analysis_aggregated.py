import pandas as pd

# Load the two input CSV files
df1 = pd.read_csv('data/output/material/03_feature_analysis/01_development_set.csv')   # Replace with actual path
df2 = pd.read_csv('data/output/material/03_feature_analysis/02_holdout_set.csv')  # Replace with actual path

# Combine both DataFrames
combined_df = pd.concat([df1, df2], ignore_index=True)

# Group by 'KBOB Category' and compute the average f0.5_score and sample count
summary_df = combined_df.groupby('Type').agg(
    **{
        'Average F0.5 Score': ('f0.5_score', 'mean'),
        'Number of Samples': ('f0.5_score', 'count')
    }
).reset_index()

# Save the result to a new CSV file
output_path = 'data/output/material/03_feature_analysis/material_type_feature.csv'  # Change if needed
summary_df.to_csv(output_path, index=False)

print(f"Summary saved to {output_path}")
