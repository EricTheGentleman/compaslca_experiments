import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Load CSV
df = pd.read_csv("data/output/category/01_samples_test/bootstrap/pairwise_CI/success_bootstrap_pairwise_vs_baseline.csv")

# Determine if CI is entirely above zero
df['positive_CI'] = (df['95%_CI_low'] > 0)

# Sort by ΔF05 and preserve order
df_sorted = df.sort_values('Δsuccess_vs_baseline', ascending=True).reset_index(drop=True)

### === PLOT 1: ΔF05 with Confidence Intervals (Bracketed, Colored) === ###
plt.figure(figsize=(8, 14))
sns.set_theme(style="whitegrid")
ax = plt.gca()

def get_color(row):
    ci_low = row['95%_CI_low']
    ci_high = row['95%_CI_high']
    if ci_low > 0:
        return 'blue'         # definitely better than baseline
    elif ci_high <= 0:
        return 'red'      # definitely worse than baseline
    else:
        return 'darkred'       # uncertain effect

# Plot CIs with bracket caps and central points
for i, row in df_sorted.iterrows():
    color = get_color(row)
    ci_low = row['95%_CI_low']
    ci_high = row['95%_CI_high']
    delta = row['Δsuccess_vs_baseline']

    # Line
    ax.plot([ci_low, ci_high], [i, i], color=color, linewidth=2)

    # Bracket caps
    cap_width = 0.2
    ax.plot([ci_low, ci_low], [i - cap_width, i + cap_width], color=color, linewidth=2)
    ax.plot([ci_high, ci_high], [i - cap_width, i + cap_width], color=color, linewidth=2)

    # Central point
    ax.plot(delta, i, 'o', color=color, markersize=4)

# Red vertical baseline at x = 0
ax.axvline(x=0, color='green', linestyle='--', linewidth=1.5)

# Y-axis labels
ax.set_yticks(range(len(df_sorted)))
ax.set_yticklabels(df_sorted['prompt'])

# Labels and legend
ax.set_title("ΔSuccess vs Baseline with 95% Confidence Intervals")
ax.set_xlabel("ΔSuccess vs Baseline")
ax.set_ylabel("Run")

# Save plot
plt.tight_layout()
plt.savefig("data/output/category/01_samples_test/plots/category_test_samples_deltaS_vs_baseline.png", dpi=400)
plt.close()



### === PLOT 2: Approximate p-values === ###
plt.figure(figsize=(4, 14))
sns.set_theme(style="whitegrid")
ax = plt.gca()

# Plot p-values as crosses
for i, row in df_sorted.iterrows():
    ax.plot(row['approx_p_value'], i, 'x', color='black', markersize=6)

# Red vertical threshold line at p = 0.05
ax.axvline(x=0.05, color='red', linestyle='--', linewidth=1)

# Match y-axis labels and order
ax.set_yticks(range(len(df_sorted)))
ax.set_yticklabels(df_sorted['prompt'])

# Labels
ax.set_title("Approx. p-values per Run")
ax.set_xlabel("Approx. p-value")
ax.set_ylabel("Run")

# Save second plot
plt.tight_layout()
plt.savefig("data/output/category/01_samples_test/plots/category_test_samples_pvalues.png", dpi=400)
plt.close()

### === PLOT 3: Configuration Table === ###
# Extract 6-bit config from prompt (assuming last 6 characters after underscore)
df_sorted['bitstring'] = df_sorted['prompt'].str.extract(r'_(\d{7})')

# Split bits into separate columns
bit_cols = [f'bit{i}' for i in range(7)]
bit_data = df_sorted['bitstring'].apply(lambda x: pd.Series(list(x), index=bit_cols)).astype(int)

# Prepare matrix for visualization
data_matrix = bit_data.to_numpy()

# Create figure
fig, ax = plt.subplots(figsize=(6, 14))
sns.set_theme(style="whitegrid")

cmap = {0: 'wheat', 1: 'mediumslateblue'}
#cmap = {0: 'lightgrey', 1: 'forestgreen'}
color_matrix = np.vectorize(cmap.get)(data_matrix)

# Plot colored cells with fine black grid lines
for i in range(data_matrix.shape[0]):        # rows (runs)
    for j in range(data_matrix.shape[1]):    # columns (bits)
        ax.add_patch(plt.Rectangle(
            (j, i), 1, 1,
            facecolor=color_matrix[i, j]
        ))

# Set limits and ticks
ax.set_xlim(0, 7)
ax.set_ylim(0, len(df_sorted))

# Bit position labels
ax.set_xticks(np.arange(7) + 0.5)
ax.set_xticklabels([f'Bit {i+1}' for i in range(7)])

# Run labels
ax.set_yticks(np.arange(len(df_sorted)) + 0.5)
ax.set_yticklabels(df_sorted['prompt'])

# Aesthetics
ax.set_aspect(0.5)  # cells wider than tall
ax.set_title("Configuration Bit Settings per Run")
ax.tick_params(axis='both', which='both', length=0)
for spine in ax.spines.values():
    spine.set_visible(False)


# Save plot
plt.tight_layout()
plt.savefig("data/output/category/01_samples_test/plots/category_test_samples_configurations.png", dpi=400)
plt.close()