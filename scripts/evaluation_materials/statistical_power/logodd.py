import numpy as np

# -----------------------------
# 0. PILOT-BASED CHANGES
# -----------------------------

"""
These are empirically observed probabilities of the outcome from a pilot study.
logit_off is the log-odds of the outcome when all predictors are 0
logit_on is the log-odds when all predictors are 1
delta_logit gives the combined log-odds increase when all predictors are turned on.
Provides a target effect budget for the simulated effects of individual predictors
"""

p_off = 0.523 # all_predictors_off
p_on = 0.675 # all_predictors_on
logit_off = np.log(p_off / (1 - p_off))
logit_on  = np.log(p_on / (1 - p_on))
delta_logit = logit_on - logit_off


# -----------------------------
# 1. PILOT-BASED COEFFICIENT SETUP
# -----------------------------

"The raw betas come from the pilot but are confounded due to the 4 runs"
"They are normalized to a maximum weight, turning them into relative importance weights"
"Then manually, some of the weights are adjusted"


# Raw coefficients from pilot (confounded)
raw_betas = {
    'geo': 0.0487,
    'ger': 0.1673,
    'cot': 0.0487,
    'etr': 0.1673,
    'isr': 0.0487,
    'exp': 0.1673
}

# Normalize to max = 1 and manually tweak weights
max_raw = max(raw_betas.values())
relative_weights = {k: v / max_raw for k, v in raw_betas.items()}


# Domain-informed adjustments
relative_weights['exp'] = 1.2   # assume exp has more influence
relative_weights['etr'] = 0.9   # etr slightly less
# leave others as is

total_relative_weight = sum(relative_weights.values())

# Set max desired log-odds effect (based on domain, ~35% OR increase)
max_effect = delta_logit / total_relative_weight
effect_sizes = {k: v * max_effect for k, v in relative_weights.items()}

print(max_effect)