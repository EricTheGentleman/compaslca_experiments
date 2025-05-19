import numpy as np
import pandas as pd
import statsmodels.api as sm

# Create pilot dataset. These are real results from runs with this configuration
pilot_data = pd.DataFrame([
    {"X1":0, "X2":0, "X3":0, "X4":0, "X5":0, "X6":0, "rate":0.52},
    {"X1":1, "X2":0, "X3":1, "X4":0, "X5":1, "X6":0, "rate":0.593},
    {"X1":0, "X2":1, "X3":0, "X4":1, "X5":0, "X6":1, "rate":0.68},
    {"X1":1, "X2":1, "X3":1, "X4":1, "X5":1, "X6":1, "rate":0.68},
])

# Simulate 191 samples per pattern (binomial approximation)
n = 191
pilot_data["Y"] = (pilot_data["rate"] * n).astype(int)
pilot_data["N"] = n

# Fit logistic regression on aggregated binomial data
X = pilot_data[["X1", "X2", "X3", "X4", "X5", "X6"]]
X = sm.add_constant(X)
y = pilot_data[["Y", "N"]]

model = sm.GLM(y, X, family=sm.families.Binomial()).fit()
print(model.summary())
