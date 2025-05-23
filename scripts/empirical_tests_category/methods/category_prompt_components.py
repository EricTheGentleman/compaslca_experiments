category_prompt_components = {

# ===================================
# === PROMPT REASONING STRATEGIES ===
# ===================================

    # VARIABLE 3: Chain of Thought Reasoning
    # Should the LLM be instructed to think "step-by-step"
    "chain_of_thought": "- Include Chain-of-Thought Reasoning. Analyze all possible categories and think step by step before making your decision.",

    # VARIABLE 4: Extract-Then-Reason
    # Should the LLM identify and summarize the key information for material inference first?
    "extract_then_reason": '''
**Extract Key Information First**
- In the first input that describes the IFC data, there is a lot of information that might not be relevant for category inference.
- Before matching a category, extract the key information that could be relevant for category inference. 
- Write the a concise summary of the key information in the "Key Information Summary" field in the required output format.
''',

    # VARIBLE 5: Iterative Self-Refinement
    # Should the LLM give a preliminary answer first, and then evaluate it / improve upon its answer?
    "iterative_self_refinement": '''
**Iterative Self Refinement**
- First, produce an output in the "Preliminary Selection" field.
- Then analyze your own output critically.
- Finally, revise your answer into a final improved version in the "Matched Category" field.
''',

# ================================
# === PROMPT CONTEXTUALIZATION ===
# ================================

    # VARIABLE 6
    # EXAMPLES
    "examples": '''
**Example 1: Clear Match**    
- If the Material Descriptor or Element Name in the IFC data mentions "Concrete", "Insulation", "Wood", "Brick", etc., then match the corresponding category.

**Example 2: Implicit Match**
- If the IFC input is somewhat vague, and it can be deduced that it is for instance a "floor covering" without specifically mentioning it, then the corresponding category is still matched.
- Same applies for other types of IFC inputs. If there is enough data such that only one category could be potentially matched, then that category should be matched.

**Example 3: True Negative**
- If the IFC input specifies the entity IfcSlab, IfcWall, etc. but there is no indication in the material data or metadata for the type of construction or material, then no category should be matched.
- In general, if the IFC input has too little data to classify it reliably into a category, then no category should be matched.
''',
 
# ======================
# === OUTPUT FORMATS ===
# ======================
# Slightly redundant to write all of them down
# But this is the best workaround with reagards to modular and nested strings

    # Output Format Baseline
    "output_format_baseline": '''
### **Required JSON Output Format:**
**DO NOT** include explanations, commentary, or markdown formatting.
Respond with **valid JSON only**, in the **exact format shown below**:
```json
{{
"Matched Category": "<Chosen Category>"
}}
```
If no viable match is found, return "None" for the "Matched Category" key:
```json
{{
"Matched Category": "None"
}}
```
''',

    # Output Format extract_then_reason == True
    "output_format_etr": '''
### **Required JSON Output Format:**
**DO NOT** include explanations, commentary, or markdown formatting.
Respond with **valid JSON only**, in the **exact format shown below**:
```json
{{
"Key Information Summary": "<Short summary of Key Information>",
"Matched Category": "<Chosen Category>"
}}
```
If no viable match is found, return "None" for the "Matched Category" key:
```json
{{
"Key Information Summary": "<Short summary of Key Information>",
"Matched Category": "None"
}}
```
''',

    # Output Format Iterative Self Refinement == True
    "output_format_irs": '''
### **Required JSON Output Format:**
**DO NOT** include explanations, commentary, or markdown formatting.
Respond with **valid JSON only**, in the **exact format shown below**:
```json
{{
"Preliminary Selection": "<Preliminary Category Choice>",
"Matched Category": "<Final Category Choice>"
}}
```
If no viable match is found, return "None" for the "Matched Category" key:
```json
{{
"Preliminary Selection": "<Preliminary Category Choice | None>",
"Matched Category": "None"
}}
```
''',

    # Output Format etr AND isr == True
    "output_format_etr_isr": '''
### **Required JSON Output Format:**
**DO NOT** include explanations, commentary, or markdown formatting.
Respond with **valid JSON only**, in the **exact format shown below**:
```json
{{
"Key Information Summary": "<Short summary of Key Information>",
"Preliminary Selection": "<Preliminary Category Choice>",
"Matched Category": "<Final Category Choice>"
}}
```
If no viable match is found, return "None" for the "Matched Category" key:
```json
{{
"Key Information Summary": "<Short summary of Key Information>",
"Preliminary Selection": "<Preliminary Category Choice | None>",
"Matched Category": "None"
}}
```
'''
}