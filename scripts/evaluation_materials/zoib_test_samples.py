"""
Light-weight ZOIB-style analysis of F0.5-scores
-----------------------------------------------
* Logistic 1 vs (0–1)        -> Pr(F = 1)
* Logistic 0 vs (0–1)        -> Pr(F = 0)
* Beta GLM on 0 < F < 1      -> E[F | 0 < F < 1]
Requires:  pandas, statsmodels ≥ 0.14, numpy
-----------------------------------------------
"""

import re
import pathlib
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.genmod.families import Beta, links

# ----------------------------------------------------------------------
# 1.  Load all 64 CSVs and parse the six on/off flags from the filename
# ----------------------------------------------------------------------
ROOT = pathlib.Path(
    "data/output/material/01_samples_test/runs_csv"
)  # adjust if needed

OUTPUT_DIR = pathlib.Path("data/output/material/01_samples_test/zoib")  # or any custom path
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  # create it if it doesn't exist


records = []
pat = re.compile(
    r"run_\d+_([ft])_([ft])_([ft])_([ft])_([ft])_([ft])\.csv", re.I
)

for csv_path in ROOT.glob("run_*_*.csv"):
    m = pat.match(csv_path.name)
    if not m:
        print(f"Skipped {csv_path.name} – name does not match pattern")
        continue
    flags = [1 if x.lower() == "t" else 0 for x in m.groups()]

    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        records.append(
            dict(
                f05=row["f0.5_score"],
                sample=row["filename"],  # so you can cluster later if desired
                flag1=flags[0],
                flag2=flags[1],
                flag3=flags[2],
                flag4=flags[3],
                flag5=flags[4],
                flag6=flags[5],
            )
        )

data = pd.DataFrame.from_records(records)
print(f"Loaded {len(data):,} rows")

# ----------------------------------------------------------------------
# 2.  Build design matrix X (intercept + 6 dummies)
# ----------------------------------------------------------------------
X = sm.add_constant(
    data[["flag1", "flag2", "flag3", "flag4", "flag5", "flag6"]], prepend=True
)

# ----------------------------------------------------------------------
# 3.  Component A – perfect matches  (F == 1)
# ----------------------------------------------------------------------
data["is_one"] = (data.f05 == 1).astype(int)
logit_one = sm.Logit(data.is_one, X).fit(disp=False)
print("\n=== P(F = 1)  – Logit model ===")
print(logit_one.summary())

# ----------------------------------------------------------------------
# 4.  Component B – total misses (F == 0)
# ----------------------------------------------------------------------
data["is_zero"] = (data.f05 == 0).astype(int)
logit_zero = sm.Logit(data.is_zero, X).fit(disp=False)
print("\n=== P(F = 0)  – Logit model ===")
print(logit_zero.summary())

# ----------------------------------------------------------------------
# 5.  Component C – Beta regression for 0 < F < 1
#     (statsmodels’ GLM Beta family needs y strictly inside (0,1))
# ----------------------------------------------------------------------
frac = data[(data.f05 > 0) & (data.f05 < 1)].copy()
# Slight “shrink” keeps values strictly inside (0,1) without altering means
eps = 1e-6
frac["f05_shrunk"] = (frac.f05 * (len(frac) - 1) + 0.5) / len(frac)
X_frac = sm.add_constant(
    frac[["flag1", "flag2", "flag3", "flag4", "flag5", "flag6"]], prepend=True
)
beta_mod = sm.GLM(
    frac.f05_shrunk,
    X_frac,
    family=Beta(link=links.logit()),  # logit link for the mean
).fit()
print("\n=== 0 < F < 1  – Beta GLM ===")
print(beta_mod.summary())

# ----------------------------------------------------------------------
# 6.  Quick eye-ball summary of main effects
# ----------------------------------------------------------------------
def tidy_res(res, label):
    out = res.params.to_frame("coef")
    out["se"] = res.bse
    out["z"] = out.coef / out.se
    out["p"] = res.pvalues
    out["component"] = label
    return out.reset_index().rename(columns={"index": "term"})


summary_df = (
    pd.concat(
        [
            tidy_res(logit_one, "prob_1"),
            tidy_res(logit_zero, "prob_0"),
            tidy_res(beta_mod, "beta_mean"),
        ],
        ignore_index=True,
    )
    .loc[lambda d: d.term != "const"]
    .sort_values(["component", "term"])
)

summary_path = OUTPUT_DIR / "main_effects_summary.csv"
summary_df.to_csv(summary_path, index=False)
logit_one.save(OUTPUT_DIR / "logit_P1.pickle")
logit_zero.save(OUTPUT_DIR / "logit_P0.pickle")
beta_mod.save(OUTPUT_DIR / "beta_model.pickle")
print(f"\nSaved summary to {summary_path}")

