import pandas as pd

# Load your CSV
df = pd.read_csv("data/input/category_test/ground_truth/Samples.csv")

# Define binning function
def bin_entries(count):
    if count == 0:
        return "0"
    elif count in [1, 2]:
        return "1-2"
    elif 2 < count <= 5:
        return "2-5"
    elif 5 < count <= 10:
        return "5-10"
    elif 10 < count <= 15:
        return "10-15"
    else:
        return "15+"

# Apply the function to create new column
df["Entries Bin"] = df["Entries Count"].apply(bin_entries)

# Save updated CSV
df.to_csv("data/input/category_test/ground_truth/Samples.csv", index=False)
