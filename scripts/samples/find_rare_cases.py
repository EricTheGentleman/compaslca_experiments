import pandas as pd

# Load your CSV file
csv_path = "data/input/category_test/ground_truth/Samples.csv"  # <-- Update this
df = pd.read_csv(csv_path)

# Define the attributes you're using for stratification
attributes = [
    "Matching Scenario",
    "KBOB Category",
    "Type",
    "Design Stage",
    "Model",
    "Data Structure",
    "Language"
]

# Create composite stratification key
df["strat_key"] = df[attributes].astype(str).agg("_".join, axis=1)

# Count how often each combination appears
value_counts = df["strat_key"].value_counts()

# Filter those that occur only once
rare_classes = value_counts[value_counts == 1]

# Show results
print(f"Found {len(rare_classes)} rare stratification groups (only 1 sample each):")
print(rare_classes)

# Optionally inspect the full rows for those rare keys
print("\nCorresponding sample rows:\n")
print(df[df["strat_key"].isin(rare_classes.index)])
