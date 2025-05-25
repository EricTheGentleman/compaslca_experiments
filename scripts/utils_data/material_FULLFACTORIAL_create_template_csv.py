import pandas as pd
from itertools import product

# === Configuration ===
output_csv = "data/output/material/01_samples_test/material_test_matrix_FFD_full.csv"  # Path to save the CSV
factor_names = ["geo", "ger", "cot", "etr", "isr", "exp"]  # Custom factor names

# Generate full factorial design (2 levels per factor, 64 runs for 6 factors)
full_factorial = list(product([0, 1], repeat=6))

# Build DataFrame
df = pd.DataFrame(full_factorial, columns=factor_names)
df.insert(0, "Run", [f"run_{i+1}" for i in range(len(df))])

# Save to CSV
df.to_csv(output_csv, index=False)
print(f"CSV saved to: {output_csv}")
