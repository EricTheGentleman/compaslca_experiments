import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
import hashlib

# Load your data
csv_path = "data/input/category_test/ground_truth/Samples.csv"  # <-- Update this
df = pd.read_csv(csv_path)

# Attributes in priority order
attributes = [
    "Matching Scenario",
    "KBOB Category",
    "Type",
    "Design Stage",
    "Language"
    #"Data Structure"
    #"Model"
]

# Composite strat key
df["strat_key"] = df[attributes].astype(str).agg("_".join, axis=1)
df["strat_label"] = df["strat_key"].apply(lambda x: int(hashlib.md5(x.encode()).hexdigest(), 16) % (10 ** 8))

# Split rare and stratifiable sets
key_counts = df["strat_key"].value_counts()
rare_keys = key_counts[key_counts == 1].index
df_rare = df[df["strat_key"].isin(rare_keys)].copy()
df_strat = df[~df["strat_key"].isin(rare_keys)].copy()

# --- Stratify main set ---
strat_split = StratifiedShuffleSplit(n_splits=1, test_size=62, random_state=42)

for train_idx, test_idx in strat_split.split(df_strat, df_strat["strat_label"]):
    df_test = df_strat.iloc[train_idx].copy()
    df_holdout = df_strat.iloc[test_idx].copy()

# --- Add rare samples randomly ---
# Shuffle rare samples for reproducibility
df_rare = df_rare.sample(frac=1, random_state=42).reset_index(drop=True)

# Number of rare samples to add to test set
test_deficit = 140 - len(df_test)
df_test_extra = df_rare.iloc[:test_deficit]
df_holdout_extra = df_rare.iloc[test_deficit:]

# Final datasets
final_test = pd.concat([df_test, df_test_extra]).drop(columns=["strat_key", "strat_label"])
final_holdout = pd.concat([df_holdout, df_holdout_extra]).drop(columns=["strat_key", "strat_label"])

# Sanity check
assert len(final_test) == 140, f"Test set has {len(final_test)} elements, expected 140"
assert len(final_holdout) == 62, f"Hold-out set has {len(final_holdout)} elements, expected 62"

# Save results
final_test.to_csv("data/input/category_test/ground_truth/test_elements.csv", index=False)
final_holdout.to_csv("data/input/category_test/ground_truth/holdout_elements.csv", index=False)

print("✅ Stratified split complete!")