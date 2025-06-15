import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
import numpy as np


# DEVELOPMENT
csv_files = [
    "data/output/category/02_samples_holdout/runs_csv/claude_haiku_3_5.csv",
    "data/output/category/02_samples_holdout/runs_csv/claude_opus_4.csv",
    "data/output/category/02_samples_holdout/runs_csv/claude_sonnet_4.csv",
    "data/output/category/02_samples_holdout/runs_csv/gemini_2_5_flash.csv",
    "data/output/category/02_samples_holdout/runs_csv/gemini_2_5_pro.csv",
    "data/output/category/02_samples_holdout/runs_csv/openai_GPT_4o-mini.csv",
    "data/output/category/02_samples_holdout/runs_csv/openai_GPT_4o.csv",
    "data/output/category/02_samples_holdout/runs_csv/openai_GPT-4_1_mini.csv",
    "data/output/category/02_samples_holdout/runs_csv/openai_GPT-4_1_nano.csv",
    "data/output/category/02_samples_holdout/runs_csv/openai_GPT-4_1.csv",
    "data/output/category/02_samples_holdout/runs_csv/openai_o3.csv",
    "data/output/category/02_samples_holdout/runs_csv/openai_o3_pro.csv"
]


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
    "openai_GPT-4_1_mini.csv": "OpenAI GPT-4.1-mini",
    "openai_GPT-4_1_nano.csv": "OpenAI GPT-4.1-nano",
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

# Replace this: combined_df['f0.5_bin'] = ...
# With this: just use the 'match' column directly
combined_df['match'] = combined_df['match'].astype(int)

# Group and normalize
match_counts = (
    combined_df
    .groupby(['source_file', 'match'])
    .size()
    .reset_index(name='count')
)

match_counts['total'] = match_counts.groupby('source_file')['count'].transform('sum')
match_counts['ratio'] = match_counts['count'] / match_counts['total']

# Pivot table for plotting
pivot_df = match_counts.pivot_table(
    index='match', columns='source_file', values='ratio', fill_value=0
).reindex([0, 1])  # 0 = incorrect, 1 = correct

group_stack_order = {
    "Claude": ["Claude Opus 4", "Claude Sonnet 4", "Claude Haiku 3.5"],
    "Gemini": ["Gemini Pro 2.5", "Gemini Flash 2.5"],
    "GPT-4o": ["OpenAI GPT-4o", "OpenAI GPT-4o-mini"],
    "GPT-4.1": ["OpenAI GPT-4.1", "OpenAI GPT-4.1-mini", "OpenAI GPT-4.1-nano"],
    "o3": ["OpenAI o3-pro", "OpenAI o3"]
}

group_colors = {
    "Claude": ["#1976d2", "#64b5f6", "#bbdefb"],
    "Gemini": ["#388e3c", "#a5d6a7"],
    "GPT-4o": ["#fec44f", "#fffd00"],
    "GPT-4.1": ["#b30000", "#e34a33", "#fd8d3c"],
    "o3": ["#8e24aa", "#ce93d8"]
}

group_names = list(group_stack_order.keys())


fig, ax = plt.subplots(figsize=(10, 9))

match_classes = [0, 1]  # x-axis
n_models = len(display_order)
bar_width = 0.8 / n_models  # total width divided among models

# Create mapping from model name to color
model_colors = {}
for group, models in group_stack_order.items():
    for i, model in enumerate(models):
        model_colors[model] = group_colors[group][i]


for i, model in enumerate(display_order):
    if model not in pivot_df.columns:
        continue

    for j, match_value in enumerate(match_classes):
        height = pivot_df.loc[match_value, model]
        bar_x = match_value + i * bar_width
        color = model_colors.get(model, 'gray')

        ax.barh(
            bar_x,
            height,
            height=bar_width,
            color=color,
            edgecolor='black',
            linewidth=0.01,
            label=model if j == 1 else None  # label once for legend
        )

# Axes and legend
ax.set_yticks([0, 1])
ax.set_yticklabels(['Incorrect (0)', 'Correct (1)'], fontsize=10)
ax.set_xlabel("Ratio of Entries")
ax.set_title("Model Accuracy Distribution per Match Class (Horizontal)", fontsize=14)
ax.set_xlim(0, 1)

# De-duplicate legend
handles, labels = ax.get_legend_handles_labels()
seen = set()
deduped = [(h, l) for h, l in zip(handles, labels) if not (l in seen or seen.add(l))]
ax.legend(*zip(*deduped), bbox_to_anchor=(1.05, 1), loc='upper left', title="Model")
for x in np.arange(0.2, 1.01, 0.2):
    ax.axvline(x=x, color='lightgray', linestyle='-', linewidth=0.5, zorder=0)
plt.tight_layout()

# Save
output_dir = "data/output/category/02_samples_holdout/plots"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(os.path.join(output_dir, "match_accuracy.png"), dpi=400)
plt.savefig(os.path.join(output_dir, "match_accuracy.pdf"), dpi=400)
plt.close()
