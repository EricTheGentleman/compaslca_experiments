import pandas as pd

# Load the input CSV file
input_csv_path = 'data/output/category/01_samples_test/category_test_success_matrix.csv'
df = pd.read_csv(input_csv_path)

# Group by 'KBOB Category' and compute Mean Accuracy and Number of Samples
kbob_summary_df = df.groupby('KBOB Category').agg(
    **{
        'Mean Accuracy': ('mean', 'mean'),
        'Number of Samples': ('mean', 'count')
    }
).reset_index()

# Save the KBOB Category summary to a new CSV file
kbob_output_csv_path = 'data/output/category/03_feature_analysis/kbob_category_analysis.csv'
kbob_summary_df.to_csv(kbob_output_csv_path, index=False)

print(f"KBOB Category summary saved to {kbob_output_csv_path}")

# Group by 'Matching Scenario' and compute Mean Accuracy and Number of Samples
scenario_summary_df = df.groupby('Matching Scenario').agg(
    **{
        'Mean Accuracy': ('mean', 'mean'),
        'Number of Samples': ('mean', 'count')
    }
).reset_index()

# Save the Matching Scenario summary to a new CSV file
scenario_output_csv_path = 'data/output/category/03_feature_analysis/matching_scenario_analysis.csv'
scenario_summary_df.to_csv(scenario_output_csv_path, index=False)

print(f"Matching Scenario summary saved to {scenario_output_csv_path}")
