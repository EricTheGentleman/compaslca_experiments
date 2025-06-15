import pandas as pd
import matplotlib.pyplot as plt
import os

# Load CSV
csv_file_path = "data/output/category/02_samples_holdout/category_holdout_aggregated.csv"
df = pd.read_csv(csv_file_path)

# Custom colors for specific models
custom_colors = {
    "claude_haiku_3_5": "#bbdefb",
    "claude_opus_4": "#1976d2",
    "claude_sonnet_4": "#64b5f6",
    "gemini_2_5_flash": "#a5d6a7",
    "gemini_2_5_pro": "#388e3c",
    "openai_GPT-4_1": "#b30000",
    "openai_GPT-4_1-mini": "#e34a33",
    "openai_GPT-4_1-nano": "#fd8d3c",
    "openai_GPT_4o": "#fec44f",
    "openai_GPT_4o-mini": "#fffd00",
    "openai_o3": "#ce93d8",
    "openai_o3_pro": "#8e24aa"
}
default_color = "gray"

# Set up plot with aspect ratio
plt.figure(figsize=(8, 8))  # Aspect ratio: 3:2
ax = plt.gca()
# ax.set_aspect('equal', adjustable='box')  # Uncomment for equal scaling

# Plot each point with its color
for _, row in df.iterrows():
    color = custom_colors.get(row["model"], default_color)
    plt.scatter(row["Avg. Cost"], row["accuracy_percent"], color=color)

# Axis config
plt.xscale('log')
plt.xlabel("Avg. Cost/Inference (log scale)")
plt.ylabel("Avg. Success Rate [%]")
plt.title("Pareto Front: Avg Success vs Average Cost (Log Scale)")
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.tight_layout()

# Save to file
output_dir = "data/output/category/02_samples_holdout/plots"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "pareto_front_plot.png")
plt.savefig(output_path, dpi=300)
pdf_path = os.path.join(output_dir, "pareto_front_plot.pdf")
plt.savefig(pdf_path, dpi=300)
