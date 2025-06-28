import pandas as pd
from pyDOE2 import ff2n

# === Configuration ===
output_csv = "data/output/category/01_samples_test/category_test_matrix_FFD_res5.csv"  # Path to save the CSV
factor_names = ["geo", "ger", "cot", "etr", "isr", "exp", "mod"]  # Replace with your custom names

# Generate resolution V FFD for 6 factors (32 runs)
design_matrix = ff2n(7)[::2]
bool_matrix = ((design_matrix + 1) / 2).astype(int)  # Convert from -1/1 to 0/1

# Build DataFrame
df = pd.DataFrame(bool_matrix, columns=factor_names)
df.insert(0, "Run", [f"run_{i+1}" for i in range(len(df))])

# Save to CSV
df.to_csv(output_csv, index=False)
print(f"CSV saved to: {output_csv}")
