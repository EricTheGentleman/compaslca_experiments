import re
from pathlib import Path
import numpy as np
import pandas as pd

DATA_DIR    = Path("data/output/material/01_samples_test/runs_csv")
OUTPUT_DIR  = Path("data/output/material/01_samples_test/bootstrap/pairwise_CI")
FILE_PATTERN = "*.csv"
COL_SAMPLE   = "filename"
COL_SCORE    = "f0.5_score" # or binomial "success" for category inference
N_BOOT       = 10_000
ALPHA        = 0.05
RANDOM_SEED  = 42
BASELINE_FLAGS = "000000"

# ---------------------------------------------------------------------
# 1  Helpers
# ---------------------------------------------------------------------
def extract_run_prefix_and_binary(stem: str) -> str:
    m = re.match(r"run_(\d+)_((?:[ft]_){5}[ft])$", stem)
    if not m:
        raise ValueError(f"{stem!r} does not match run_* pattern")
    run_no = int(m.group(1))
    binary = "".join("1" if b == "t" else "0" for b in m.group(2).split("_"))
    return f"run{run_no}_{binary}"

# ---------------------------------------------------------------------
# 2  Load and align all CSVs
# ---------------------------------------------------------------------
files = sorted(DATA_DIR.glob(FILE_PATTERN))
prompt_names = [extract_run_prefix_and_binary(f.stem) for f in files]
scores_per_prompt = []

for f in files:
    df = pd.read_csv(f)
    df = df.sort_values(COL_SAMPLE)
    scores_per_prompt.append(df[COL_SCORE].to_numpy(float))

n_samples_set = {arr.size for arr in scores_per_prompt}
n_samples = n_samples_set.pop()

scores = np.vstack(scores_per_prompt)
n_prompts = scores.shape[0]

# ---------------------------------------------------------------------
# 3  Bootstrap sampling
# ---------------------------------------------------------------------
rng = np.random.default_rng(RANDOM_SEED)
boot_means = np.empty((N_BOOT, n_prompts), float)

for b in range(N_BOOT):
    idx = rng.choice(n_samples, n_samples, replace=True)
    boot_means[b] = scores[:, idx].mean(axis=1)

# ---------------------------------------------------------------------
# 4  Pairwise vs BASELINE
# ---------------------------------------------------------------------

baseline_prompt = next(p for p in prompt_names if p.endswith(f"_{BASELINE_FLAGS}"))
baseline_idx  = prompt_names.index(baseline_prompt)
baseline_boot = boot_means[:, baseline_idx]

rows_base = []
for name in prompt_names:
    if name == baseline_prompt:
        continue
    idx  = prompt_names.index(name)
    diff = boot_means[:, idx] - baseline_boot
    ci_lo, ci_hi = np.percentile(diff, [100*ALPHA/2, 100*(1-ALPHA/2)])
    p_val = 2 * min((diff < 0).mean(), (diff > 0).mean())
    rows_base.append((name, diff.mean(), ci_lo, ci_hi, p_val))

diff_base_df = pd.DataFrame(
    rows_base,
    columns=["prompt", "ΔF05_vs_baseline",
             f"{int((1-ALPHA)*100)}%_CI_low",
             f"{int((1-ALPHA)*100)}%_CI_high",
             "approx_p_value"],
).set_index("prompt")

# ---------------------------------------------------------------------
# 5  Save Results
# ---------------------------------------------------------------------
diff_base_df.to_csv(OUTPUT_DIR / "F05_bootstrap_pairwise_vs_baseline.csv")