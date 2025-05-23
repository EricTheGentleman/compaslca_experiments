import pandas as pd
import matplotlib.pyplot as plt

# Path to your CSV file
csv_file = "data/input/category_test/ground_truth/test_elements.csv"

# Columns to generate pie charts for
columns_of_interest = [
    "KBOB Category",
    "Type",
    "Matching Scenario",
    "Data Structure",
    "Model",
    "Design Stage",
    "Language",
    "Entries Count"
]

# Load CSV data
df = pd.read_csv(csv_file)

# Font size settings
legend_font_size = 8
percent_font_size = 8
title_font_size = 10

# Create and save pie charts with a legend
for column in columns_of_interest:
    value_counts = df[column].value_counts(dropna=False)
    labels = value_counts.index.astype(str)
    sizes = value_counts.values

    fig, ax = plt.subplots(figsize=(7, 7))

    # Draw pie chart with no slice labels
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,  # Disable labels in slices
        autopct='%1.1f%%',
        startangle=140,
        textprops={'fontsize': percent_font_size}
    )

    # Add legend with labels and matching colors
    ax.legend(
        wedges,
        labels,
        title=column,
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=legend_font_size,
        title_fontsize=legend_font_size
    )

    # Title and layout
    plt.title(f'{column}', fontsize=title_font_size)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Save the figure (bbox_inches='tight' ensures the legend is not cut off)
    filename = f"data/plots/samples_test/samples_test_{column.replace(' ', '_')}.png"
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filename}")
