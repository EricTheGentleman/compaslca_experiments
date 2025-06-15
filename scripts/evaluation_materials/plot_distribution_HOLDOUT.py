import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
import numpy as np


# DEVELOPMENT
csv_files = [
    "data/output/material/02_samples_holdout/runs_csv/claude_haiku_3_5.csv",
    "data/output/material/02_samples_holdout/runs_csv/claude_opus_4.csv",
    "data/output/material/02_samples_holdout/runs_csv/claude_sonnet_4.csv",
    "data/output/material/02_samples_holdout/runs_csv/gemini_2_5_flash.csv",
    "data/output/material/02_samples_holdout/runs_csv/gemini_2_5_pro.csv",
    "data/output/material/02_samples_holdout/runs_csv/openai_GPT_4o-mini.csv",
    "data/output/material/02_samples_holdout/runs_csv/openai_GPT_4o.csv",
    "data/output/material/02_samples_holdout/runs_csv/openai_GPT-4_1-mini.csv",
    "data/output/material/02_samples_holdout/runs_csv/openai_GPT-4_1-nano.csv",
    "data/output/material/02_samples_holdout/runs_csv/openai_GPT-4_1.csv",
    "data/output/material/02_samples_holdout/runs_csv/openai_o3.csv",
    "data/output/material/02_samples_holdout/runs_csv/openai_o3_pro.csv"
]
output_path = "data/output/material/02_samples_holdout/plots/materials_holdout_model_distribution12.png"

# Combine data from all CSVs
all_data = []

for file in csv_files:
    df = pd.read_csv(file)
    df['source_file'] = os.path.basename(file)
    all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)

# Define a custom name mapping

name_mapping = {
    "claude_haiku_3_5.csv": "Claude Haiku 3.5",
    "claude_opus_4.csv": "Claude Opus 4",
    "claude_sonnet_4.csv": "Claude Sonnet 4",
    "gemini_2_5_flash.csv": "Gemini Flash 2.5",
    "gemini_2_5_pro.csv": "Gemini Pro 2.5",
    "openai_GPT_4o-mini.csv": "OpenAI GPT-4o-mini",
    "openai_GPT_4o.csv": "OpenAI GPT-4o",
    "openai_GPT-4_1-mini.csv": "OpenAI GPT-4.1-mini",
    "openai_GPT-4_1-nano.csv": "OpenAI GPT-4.1-nano",
    "openai_GPT-4_1.csv": "OpenAI GPT-4.1",
    "openai_o3.csv": "OpenAI o3",
    "openai_o3_pro.csv": "OpenAI o3-pro"
}

# After loading and combining your data
combined_df['source_file'] = combined_df['source_file'].map(name_mapping)

# In the bin_counts dataframe, source_file now holds display names
# Use the same display names in the desired order
display_order = [
    "OpenAI GPT-4o-mini",
    "OpenAI GPT-4o",
    "OpenAI GPT-4.1-nano",
    "OpenAI GPT-4.1-mini",
    "OpenAI GPT-4.1",
    "OpenAI o3",
    "OpenAI o3-pro",
    "Gemini Flash 2.5",
    "Gemini Pro 2.5",
    "Claude Haiku 3.5",
    "Claude Sonnet 4",
    "Claude Opus 4"
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
model_color_map = {

    # GPT-4o group - blue shades
    "OpenAI GPT-4o-mini":  "#fffd00",   # light blue
    "OpenAI GPT-4o":       "#fec44f",   # standard blue

    # GPT-4.1 group - yellow shades
    "OpenAI GPT-4.1-nano": "#fd8d3c",   # light yellow
    "OpenAI GPT-4.1-mini": "#e34a33",   # standard yellow
    "OpenAI GPT-4.1":      "#b30000",   # deeper yellow

    # GPT-o3 group - purple shades
    "OpenAI o3":           "#ce93d8",   # light purple
    "OpenAI o3-pro":       "#8e24aa",   # dark purple

    # Gemini group - green shades
    "Gemini Pro 2.5":      "#388e3c", # light green
    "Gemini Flash 2.5":    "#a5d6a7",   # dark green

    # Claude group - orange shades
    "Claude Haiku 3.5":    "#bbdefb",   # light orange
    "Claude Sonnet 4":     "#64b5f6",   # medium orange
    "Claude Opus 4":       "#1976d2",   # deep orange
}



# Plot
plt.figure(figsize=(9, 5))
sns.set_theme(style="whitegrid")

ax = sns.barplot(
    data=bin_counts,
    x="f0.5_bin",
    y="ratio",
    hue="source_file",
    palette=model_color_map
)
plt.ylim(0, 0.5)

plt.xticks(fontsize=9)
plt.yticks(fontsize=9)
plt.ylabel('Ratio of Entries')
plt.xlabel('f0.5 Score Bin')
plt.title('Distribution of f0.5 Scores by File (Custom Bins)')
#ax.legend_.remove()
plt.legend(title='CSV File', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(output_path, dpi=400)
plt.close()



