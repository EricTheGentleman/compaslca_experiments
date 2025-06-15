import matplotlib.pyplot as plt
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



# Step 1: Define model groupings and stack order (top model first!)
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
bin_order = ['0.0', '(0-0.2]', '(0.2-0.4]', '(0.4-0.6]', '(0.6-0.8]', '(0.8-1.0)', '1.0']

# Step 2: Pivot data
pivot_df = bin_counts.pivot_table(
    index='f0.5_bin', columns='source_file', values='ratio', fill_value=0
).reindex(bin_order)

fig, ax = plt.subplots(figsize=(10, 9))

y_bins = np.arange(len(bin_order))  # 7 bins total
group_width = 0.8  # total vertical space per bin
n_groups = len(group_names)
group_spacing = group_width / n_groups

group_to_index = {group: i for i, group in enumerate(group_names)}

for bin_i, bin_label in enumerate(bin_order):
    for group in group_names:
        group_models = group_stack_order[group]
        group_index = group_to_index[group]

        # Compute base y position for this group in this bin
        base_y = bin_i - group_width / 2 + group_index * group_spacing + group_spacing / 2

        # Get model ratios for this bin
        model_ratios = []
        for model in group_models:
            if model in pivot_df.columns:
                ratio = pivot_df.loc[bin_label, model]
                model_ratios.append((model, ratio))

        # Sort: largest drawn first (back), smallest last (front)
        model_ratios_sorted = sorted(model_ratios, key=lambda x: -x[1])

        # Plot each model bar
        for zorder, (model, ratio) in enumerate(model_ratios_sorted):
            color_index = group_stack_order[group].index(model)
            color = group_colors[group][color_index]
            ax.barh(
                base_y,
                ratio,
                height=group_spacing * 0.9,
                color=color,
                label=model if bin_i == 0 else None,
                zorder=zorder+2,
                edgecolor='black',
                linewidth=0.01,
                alpha=1
            )

# Set axis layer behavior
ax.set_axisbelow(True)

# Manually draw vertical grid lines at desired x-ticks
xticks = np.arange(0, 0.6 + 0.1, 0.1)
for xtick in xticks:
    ax.axvline(x=xtick, color='lightgray', linestyle='-', linewidth=0.3, zorder=1)

# (Optional) customize ticks too
ax.set_xticks(xticks)
# Axis formatting
ax.set_yticks(y_bins)
ax.set_yticklabels(bin_order, fontsize=9)
ax.set_xlabel("Ratio of Entries")
ax.set_ylabel("f0.5 Score Bin")
ax.set_title("Grouped Overlapping Distribution of f0.5 Scores by Model")
ax.set_xlim(0, 0.5)

# Legend de-duplication
handles, labels = ax.get_legend_handles_labels()
seen = set()
deduped = [(h, l) for h, l in zip(handles, labels) if not (l in seen or seen.add(l))]
ax.legend(*zip(*deduped), bbox_to_anchor=(1.05, 1), loc='upper left', title="Model")

plt.tight_layout()

# Save
output_dir = "data/output/material/02_samples_holdout/plots"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(os.path.join(output_dir, "grouped_overlapping_f05_distribution_horizontal.png"), dpi=400)
plt.savefig(os.path.join(output_dir, "grouped_overlapping_f05_distribution_horizontal.pdf"), dpi=400)
plt.close()
