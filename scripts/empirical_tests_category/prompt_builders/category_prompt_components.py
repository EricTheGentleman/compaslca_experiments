category_prompt_components = {

    # ========================================
    # === Family 3: prompt farming & style ===
    # ========================================

    # Emphasize expert role
    "expert_role_emphasis": "You are an expert in conducting life cycle assessment (LCA) on BIM elements and an expert in material classification. ",

    # How should the task be framed?
    "content_framing": "Accuracy matters a lot! Incorrect answers will strongly impact important downstream processes.",

    # Should the LLM justify it's decision at the end?
    "decision_justification": '''
**Decision Justification**
- After choosing a category, include a short decision justification in the corresponding output field.
- Highlight any textual clues (like element name or material descriptors), geometric properties, or property sets that were useful in matching the element to the chosen category.
- Keep the explanation clear and concise.
''',

    # How efficient/thorough should it be?
    "analysis_granularity_efficient": "Respond quickly and concisely. Minimize latency and token usage by focusing only on the most relevant fields.",
    "analysis_granularity_thorough": "Latency and token usage are not a concern — prioritize completeness and rigor in your reasoning.",

    # ===========================================
    # === Family 4: prompt reasoning strategy ===
    # ===========================================

    # Chain of Thought Reasoning
    "chain_of_thought": "Include Chain-of-Thought Reasoning. Analyze all possible entries and think step by step before making your decision.",

    # Should the LLM give a preliminary answer first, and then evaluate it / improve upon its answer?
    "iterative_self_refinement": '''
**Iterative Self Refinement**
- First, produce a output in the preliminary matched category field.
- Then analyze your own output critically.
- Finally, revise your answer into a final improved version in the matched category field.
''',

    # Should the LLM summarize the most important parts first?
    "summarize_first": '''
**Summarize the Key Information**
- Within the JSON file that describes the BIM data, there is a lot of information that might not be relevant for category inference.
- Before matching a category, summarize the key information that could be relevant for the category inference. 
- Write the summary in the respective key information summary field in the required output format.
''',

    # ===================================
    # === Family 5: Scenario Emphasis ===
    # ===================================

    # Provide the matching scenarios
    "scenario_explanation": '''
**Matching Scenarios**
- If the available data is insufficient to support a confident match, assign the category "None".
- If the BIM data represents a compound system (e.g., a layered floor or wall build-up without clear material separation), assign the category "None".
- Only assign a category if there is enough reliable data to justify a confident match.
''',

    # Should the LLM emphasize certain data?
    "data_emphasis_meta": "Before analyzing the full BIM data, prioritize and interpret the value of the Element Metadata key as an important input for category inference",
    "data_emphasis_mat": "Before analyzing the full BIM data, prioritize and interpret the material descriptors as an important input for category inference",
    "data_emphasis_geom": "Before analyzing the full BIM data, prioritize and interpret the value of the Element Geometry key as an important input for category inference",
    "data_emphasis_pset": "Before analyzing the full BIM data, prioritize and interpret the value of the Element Property Sets key as an important input for category inference",


    # ======================
    # === OUTPUT FORMATS ===
    # ======================
    # Slightly redundant to write all of them down
    # But this is the best workaround with reagards to modular and nested strings

    # Output Format Baseline
    "output_format_baseline": '''
### **Required JSON Output Format:**
Respond **ONLY** with valid JSON in the exact format below:
```json
{{
"Matched Category": "<Chosen Category>"
}}
```
**DO NOT** include additional explanations, commentary, or markdown formatting.
"""
''',

    # Output Format Decision Justification == True
    "output_format_dj": '''
### **Required JSON Output Format:**
Respond **ONLY** with valid JSON in the exact format below:
```json
{{
"Matched Category": "<Chosen Category>",
"Decision Justification": "<Insert decision justification here>"
}}
```
**DO NOT** include additional explanations, commentary, or markdown formatting.
"""
''',

    # Output Format Iterative Self Refinement == True
    "output_format_isr": '''
### **Required JSON Output Format:**
Respond **ONLY** with valid JSON in the exact format below:
```json
{{
"Preliminary Matched Category": "<Chosen Category>",
"Matched Category": "<Chosen Category after self-refinement>"
}}
```
**DO NOT** include additional explanations, commentary, or markdown formatting.
"""
''',

    # Output Format Summarize First == True
    "output_format_sf": '''
### **Required JSON Output Format:**
Respond **ONLY** with valid JSON in the exact format below:
```json
{{
"Key Information Summary": "<Summarize your findings with regards to the key information for category inference>",
"Matched Category": "<Chosen Category>"
}}
```
**DO NOT** include additional explanations, commentary, or markdown formatting.
"""
''',

    # Output Format isr/sf
    "output_format_isr_sf": '''
### **Required JSON Output Format:**
Respond **ONLY** with valid JSON in the exact format below:
```json
{{
"Key Information Summary": "<Summarize your findings with regards to the key information for category inference>",
"Preliminary Matched Category": "<Chosen Category>",
"Matched Category": "<Chosen Category after self-refinement>"
}}
```
**DO NOT** include additional explanations, commentary, or markdown formatting.
"""
''',

    # Output Format dj/sf:
    "output_format_dj_sf": '''
### **Required JSON Output Format:**
Respond **ONLY** with valid JSON in the exact format below:
```json
{{
"Key Information Summary": "<Summarize your findings with regards to the key information for category inference>",
"Matched Category": "<Chosen Category>",
"Decision Justification": "<Insert decision justification here>"
}}
```
**DO NOT** include additional explanations, commentary, or markdown formatting.
"""
''',

    # Output Format dj/isr:
    "output_format_dj_sf": '''
### **Required JSON Output Format:**
Respond **ONLY** with valid JSON in the exact format below:
```json
{{
"Preliminary Matched Category": "<Chosen Category>",
"Matched Category": "<Chosen Category after self-refinement>",
"Decision Justification": "<Insert decision justification here>"
}}
```
**DO NOT** include additional explanations, commentary, or markdown formatting.
"""
''',

    # Output Format dj/isr/sf:
    "output_format_dj_sf": '''
### **Required JSON Output Format:**
Respond **ONLY** with valid JSON in the exact format below:
```json
{{
"Key Information Summary": "<Summarize your findings with regards to the key information for category inference>",
"Preliminary Matched Category": "<Chosen Category>",
"Matched Category": "<Chosen Category after self-refinement>",
"Decision Justification": "<Insert decision justification here>"
}}
```
**DO NOT** include additional explanations, commentary, or markdown formatting.
"""
''',

}
