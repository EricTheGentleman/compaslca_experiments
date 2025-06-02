"""
bootstrap_f0_5.py

Compute macro-F0.5 means and 95 % paired-bootstrap CIs for 64 prompt
configurations, and (optionally) pairwise differences to the best prompt.

Filestore layout (example)
--------------------------
data/output/pipeline/01_samples_test/
 ├─ runs_csv/                # 64 raw CSVs, one per prompt
 └─ bootstrap/pairwise_CI/   # this script writes its artefacts here
      ├─ bootstrap_results_per_prompt.csv
      ├─ bootstrap_pairwise_vs_best.csv
      ├─ boot_means.npz
      └─ bootstrap_uncertainty_topN.png
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------
# 0  Settings
# ---------------------------------------------------------------------
DATA_DIR    = Path("data/output/material/02_samples_holdout/runs_csv")
FILE_PATTERN = "*.csv"

COL_SAMPLE  = "filename"          # row identifier in every CSV
COL_SCORE   = "f0.5_score"    # per-sample F0.5 column

N_BOOT      = 10_000
ALPHA       = 0.05
RANDOM_SEED = 42

BASELINE_FLAGS = "000000"     # ← all-false prompt you call “baseline”

OUTPUT_DIR = Path(
    "data/output/material/02_samples_holdout/bootstrap/pairwise_CI"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# 1  Helpers
# ---------------------------------------------------------------------
def extract_run_prefix_and_binary(stem: str) -> str:
    # run_12_f_f_t_f_t_f → run12_001010
    m = re.match(r"run_(\d+)_((?:[ft]_){5}[ft])$", stem)
    if not m:
        raise ValueError(f"{stem!r} does not match run_* pattern")
    run_no = int(m.group(1))
    binary = "".join("1" if b == "t" else "0" for b in m.group(2).split("_"))
    return f"run{run_no}_{binary}"

# ---------------------------------------------------------------------
# 2  Load all CSVs
# ---------------------------------------------------------------------
files = sorted(DATA_DIR.glob(FILE_PATTERN))
if not files:
    raise FileNotFoundError(f"No CSVs in {DATA_DIR}")

prompt_names = [extract_run_prefix_and_binary(f.stem) for f in files]
scores_per_prompt: list[np.ndarray] = []

for f in files:
    df = pd.read_csv(f)
    if {COL_SAMPLE, COL_SCORE}.difference(df.columns):
        raise KeyError(f"{f} lacks {COL_SAMPLE} / {COL_SCORE}")
    df = df.sort_values(COL_SAMPLE)
    scores_per_prompt.append(df[COL_SCORE].to_numpy(float))

n_samples_set = {a.size for a in scores_per_prompt}
if len(n_samples_set) != 1:
    raise ValueError("CSVs have different numbers of rows")
n_samples = n_samples_set.pop()

scores = np.vstack(scores_per_prompt)           # shape: (prompts, samples)
n_prompts = scores.shape[0]
print(f"Loaded {n_prompts} prompts × {n_samples} samples")

# ---------------------------------------------------------------------
# 3  Point estimates
# ---------------------------------------------------------------------
macro_means = scores.mean(axis=1)               # (prompts,)

# ---------------------------------------------------------------------
# 4  Paired bootstrap
# ---------------------------------------------------------------------
rng = np.random.default_rng(RANDOM_SEED)
boot_means = np.empty((N_BOOT, n_prompts), float)

for b in range(N_BOOT):
    idx = rng.choice(n_samples, n_samples, replace=True)
    boot_means[b] = scores[:, idx].mean(axis=1)

np.savez_compressed(
    OUTPUT_DIR / "F0.5_boot_means.npz",
    boot_means=boot_means,
    prompt_names=np.array(prompt_names),
)
print("→ boot_means.npz saved")

# ---------------------------------------------------------------------
# 5  Per-prompt CI
# ---------------------------------------------------------------------
lower = np.percentile(boot_means, 100 * ALPHA / 2, axis=0)
upper = np.percentile(boot_means, 100 * (1 - ALPHA / 2), axis=0)

ci_df = pd.DataFrame({
    "prompt":     prompt_names,
    "macro_F1": macro_means,
    f"{int((1-ALPHA)*100)}%_CI_low":  lower,
    f"{int((1-ALPHA)*100)}%_CI_high": upper,
})

# keep natural order (run1…, run2…) for readability
ci_df["run_no"] = ci_df["prompt"].str.extract(r"run(\d+)", expand=False).astype(int)
ci_df = ci_df.sort_values("run_no").drop(columns="run_no").reset_index(drop=True)

# ---------------------------------------------------------------------
# 6  Pairwise vs BEST
# ---------------------------------------------------------------------
best_idx    = macro_means.argmax()
best_prompt = prompt_names[best_idx]
best_boot   = boot_means[:, best_idx]

rows_best = []
for name in prompt_names:
    idx  = prompt_names.index(name)
    diff = best_boot - boot_means[:, idx]               # +ve → best better
    ci_lo, ci_hi = np.percentile(diff, [100*ALPHA/2, 100*(1-ALPHA/2)])
    p_val = 2 * min((diff < 0).mean(), (diff > 0).mean())
    rows_best.append((name, diff.mean(), ci_lo, ci_hi, p_val))

diff_best_df = pd.DataFrame(
    rows_best,
    columns=["prompt", "ΔF0.5_vs_best",
             f"{int((1-ALPHA)*100)}%_CI_low",
             f"{int((1-ALPHA)*100)}%_CI_high",
             "approx_p_value"],
).set_index("prompt")

# ---------------------------------------------------------------------
# 7  Pairwise vs BASELINE
# ---------------------------------------------------------------------
try:
    baseline_prompt = next(p for p in prompt_names if p.endswith(f"_{BASELINE_FLAGS}"))
except StopIteration:
    raise ValueError(f"No prompt ends with _{BASELINE_FLAGS} (baseline)")

baseline_idx  = prompt_names.index(baseline_prompt)
baseline_boot = boot_means[:, baseline_idx]

rows_base = []
for name in prompt_names:
    if name == baseline_prompt:
        continue
    idx  = prompt_names.index(name)
    diff = boot_means[:, idx] - baseline_boot          # +ve → variant better
    ci_lo, ci_hi = np.percentile(diff, [100*ALPHA/2, 100*(1-ALPHA/2)])
    p_val = 2 * min((diff < 0).mean(), (diff > 0).mean())
    rows_base.append((name, diff.mean(), ci_lo, ci_hi, p_val))

diff_base_df = pd.DataFrame(
    rows_base,
    columns=["prompt", "ΔF0.5_vs_baseline",
             f"{int((1-ALPHA)*100)}%_CI_low",
             f"{int((1-ALPHA)*100)}%_CI_high",
             "approx_p_value"],
).set_index("prompt")

# ---------------------------------------------------------------------
# 8  Write CSVs
# ---------------------------------------------------------------------
ci_df.to_csv(OUTPUT_DIR / "F05_bootstrap_results_per_prompt.csv", index=False)
print("→ bootstrap_results_per_prompt.csv written")

diff_best_df.to_csv(OUTPUT_DIR / "F05_bootstrap_pairwise_vs_best.csv")
print(f"→ bootstrap_pairwise_vs_best.csv written (best = {best_prompt})")

diff_base_df.to_csv(OUTPUT_DIR / "F05_bootstrap_pairwise_vs_baseline.csv")
print(f"→ bootstrap_pairwise_vs_baseline.csv written (baseline = {baseline_prompt})")
