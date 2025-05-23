import pandas as pd
import matplotlib.pyplot as plt
import os

# Load CSV
df = pd.read_csv("data/input/category_test/ground_truth/Samples.csv")
df.columns = df.columns.str.strip()  # remove extra spaces

# Outer ring: Language distribution
outer_counts = df["Language"].value_counts()
outer = outer_counts.values
outer_labels = outer_counts.index

# Middle ring: Model distribution
middle_counts = df["Model"].value_counts()
middle = middle_counts.values
middle_labels = middle_counts.index

# Inner ring: Design Stage distribution
inner_counts = df["Design Stage"].value_counts()
inner = inner_counts.values
inner_labels = inner_counts.index

# === Plot ===
fig, ax = plt.subplots(figsize=(8, 8))
ax.axis('equal')

# Outer ring (Languages)
ax.pie(
    outer,
    radius=1.0,
    labels=outer_labels,
    labeldistance=1.05,
    wedgeprops=dict(width=0.2, edgecolor='white')
)

# Middle ring (Models)
ax.pie(
    middle,
    radius=0.8,
    labels=middle_labels,
    labeldistance=0.75,
    wedgeprops=dict(width=0.2, edgecolor='white')
)

# Inner ring (Design Stages)
ax.pie(
    inner,
    radius=0.6,
    labels=inner_labels,
    labeldistance=0.4,
    wedgeprops=dict(width=0.2, edgecolor='white')
)

# Save output
os.makedirs("data/plots/samples_all", exist_ok=True)
plt.title('Nested Donut Plot from CSV')
plt.savefig("data/plots/samples_all/donut_design_stage.png", dpi=300, bbox_inches='tight')
plt.show()
