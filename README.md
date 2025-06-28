# COMPAS-LCA: Empirical Tests

This repository contains all data and scripts related to the empirical tests conducted as part of the COMPAS-LCA master's thesis. The project is organized by the three steps of the Design of Experiments (DoE), as well as optional stability analysis.

---

## Repository Structure

### Input Data

**Exploration Samples (DoE Step 1):**

- `data/input/category_test/samples/samples_test/` – 140 samples for category inference.
- `data/input/materials_test/samples/samples_test/` – 136 samples for material inference.
- `data/input/category_test/samples/samples_holdout/` – 62 holdout samples for unbiased evaluation.
- `data/input/materials_test/samples/samples_holdout/` – 60 holdout samples for unbiased evaluation.

Sample stratification script:
scripts/samples/stratify_samples_holdout_vs_test.py

---

**Model Configuration (choose model, provider, API key):**

- `configs/model_config.yaml`

### Ground Truth & Reference Data

- `data/ground_truth/` – Human-annotated material matches for 202 samples.
- `data/KBOB/` – Dissected Swiss KBOB LCA database.

---

## Empirical Tests

### DoE Step 1: Prompt Configuration & Exploration

**Prompt configurations:**

- `configs/category_test/`
- `configs/material_test/`

**Output results (with bootstrapped confidence intervals):**

- `data/output/category/01_samples_test/`
- `data/output/material/01_samples_test/`

**Bootstrap scripts:**
- `scripts/evaluation_categories/CATEGORY_bootstrap.py`
- `scripts/evaluation_materials/MATERIAL_bootstrap.py`

**Test scripts:**
- `scripts/empirical_tests_category/`
- `scripts/empirical_tests_materials/`


---

### DoE Step 2: Model Evaluation on Holdout Samples

**Best configurations:**

- `configs/category_holdout/`
- `configs/material_holdout/`

**Holdout input data:**

- `data/input/category_test/samples/samples_holdout/`
- `data/input/materials_test/samples/samples_holdout/`

**Holdout results:**

- `data/output/category/02_samples_holdout/`
- `data/output/material/02_samples_holdout/`

---

### DoE Step 3: Feature Analysis

DoE Step 3 was only conducted on material inference

**Scripts:**
- `scripts/evaluation_materials/material_feature_analysis_csv.py`
- `scripts/evaluation_materials/material_feature_analysis_aggregated.py`

---

## Optional: Stability Analysis (GPT-4o)

An optional experiment (not included in the thesis) tested GPT-4o’s determinism.  
50 random samples were run 10 times through the same prompt to observe output consistency.

**Results:**

- `data/output/material/00_stability/jaccard_summary_materials.csv`
- `data/output/material/00_stability/stability_metrics.json`

---

## Notes

- A small number of category inference samples are true negatives, leading to a slightly reduced number of usable samples (136) for material inference.
- The project uses a factorial design across multiple LLMs and prompt variations to evaluate performance across categories and materials.

---