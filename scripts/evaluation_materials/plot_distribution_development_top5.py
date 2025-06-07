import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
"""
# DEVELOPMENT
csv_files = [
    "data/output/material/01_samples_test/runs_csv/run_1_f_f_f_f_f_f.csv",
    "data/output/material/01_samples_test/runs_csv/run_24_f_t_f_t_t_t.csv",
    "data/output/material/01_samples_test/runs_csv/run_50_t_t_f_f_f_t.csv",
    "data/output/material/01_samples_test/runs_csv/run_64_t_t_t_t_t_t.csv",
    "data/output/material/01_samples_test/runs_csv/run_32_f_t_t_t_t_t.csv",
    "data/output/material/01_samples_test/runs_csv/run_22_f_t_f_t_f_t.csv"
]
output_path = "data/output/material/01_samples_test/plots/materials_test_samples_distribution_top5.png"
# HOLDOUT
"""
csv_files = [
    "data/output/material/02_samples_holdout/runs_csv/run_1_f_f_f_f_f_f.csv",
    "data/output/material/02_samples_holdout/runs_csv/run_24_f_t_f_t_t_t.csv",
    "data/output/material/02_samples_holdout/runs_csv/run_50_t_t_f_f_f_t.csv",
    "data/output/material/02_samples_holdout/runs_csv/run_64_t_t_t_t_t_t.csv",
    "data/output/material/02_samples_holdout/runs_csv/run_32_f_t_t_t_t_t.csv",
    "data/output/material/02_samples_holdout/runs_csv/run_22_f_t_f_t_f_t.csv"
]
output_path = "data/output/material/02_samples_holdout/plots/materials_HO_samples_distribution_top5.png"


# Combine data from all CSVs
all_data = []

for file in csv_files:
    df = pd.read_csv(file)
    df['source_file'] = os.path.basename(file)
    all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)

# Define a custom name mapping
name_mapping = {
    "run_1_f_f_f_f_f_f.csv": "000000",
    "run_22_f_t_f_t_f_t.csv": "010101",
    "run_32_f_t_t_t_t_t.csv": "011111",
    "run_64_t_t_t_t_t_t.csv": "111111",
    "run_50_t_t_f_f_f_t.csv": "110001",
    "run_24_f_t_f_t_t_t.csv": "010111"
}

# After loading and combining your data
combined_df['source_file'] = combined_df['source_file'].map(name_mapping)

# In the bin_counts dataframe, source_file now holds display names
# Use the same display names in the desired order
display_order = [
    "000000",
    "010101",
    "011111",
    "111111",
    "110001",
    "010111"
]

# Assign custom bins
def bin_f05(score):
    if score == 0.0:
        return '0.0'
    elif 0.0 < score <= 0.2:
        return '(0-0.2]'
    elif 0.2 < score <= 0.4:
        return '(0.2-0.4]'
    elif 0.4 < score <= 0.6:
        return '(0.4-0.6]'
    elif 0.6 < score <= 0.8:
        return '(0.6-0.8]'
    elif 0.8 < score < 1.0:
        return '(0.8-1.0)'
    elif score == 1.0:
        return '1.0'
    else:
        return 'Other'

combined_df['f0.5_bin'] = combined_df['f0.5_score'].apply(bin_f05)

# Count and normalize per file
bin_counts = (
    combined_df
    .groupby(['source_file', 'f0.5_bin'])
    .size()
    .reset_index(name='count')
)

# Normalize to ratios per file
bin_counts['total'] = bin_counts.groupby('source_file')['count'].transform('sum')
bin_counts['ratio'] = bin_counts['count'] / bin_counts['total']

# Ensure fixed bin order
bin_order = ['0.0', '(0-0.2]', '(0.2-0.4]', '(0.4-0.6]', '(0.6-0.8]', '(0.8-1.0)', '1.0']
bin_counts['f0.5_bin'] = pd.Categorical(bin_counts['f0.5_bin'], categories=bin_order, ordered=True)

# Apply the new order
bin_counts['source_file'] = pd.Categorical(
    bin_counts['source_file'],
    categories=display_order,
    ordered=True
)

# Create a Seaborn palette for the remaining 5 categories
seaborn_palette = sns.color_palette("bright", n_colors=5)

# Insert your custom light-grey color for "000000"
custom_palette = {
    "000000": "#d3d3d3"  # light-grey
}

# Add the rest from seaborn_palette in the order you want
for name, color in zip(display_order[1:], seaborn_palette):  # skip "000000"
    custom_palette[name] = color

# Plot
plt.figure(figsize=(6, 3.5))
sns.set_theme(style="whitegrid")

ax = sns.barplot(
    data=bin_counts,
    x="f0.5_bin",
    y="ratio",
    hue="source_file",
    palette=custom_palette
)
plt.ylim(0, 0.6)

plt.xticks(fontsize=9)
plt.yticks(fontsize=9)
plt.ylabel('Ratio of Entries')
plt.xlabel('f0.5 Score Bin')
plt.title('Distribution of f0.5 Scores by File (Custom Bins)')
plt.legend(title='CSV File', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(output_path, dpi=400)
plt.close()



