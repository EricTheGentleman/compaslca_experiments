material_prompt_components = {

# ===================================
# === PROMPT REASONING STRATEGIES ===
# ===================================

    # VARIABLE 3: Chain of Thought Reasoning
    # Should the LLM be instructed to think "step-by-step"
    "chain_of_thought": "- Include Chain-of-Thought Reasoning. Analyze all possible material options and think step by step before making your decision.",

    # VARIABLE 4: Extract-Then-Reason
    # Should the LLM identify and summarize the key information for material inference first?
    "extract_then_reason": '''

**Extract Key Information First**
- In the first input that describes the IFC data, there is a lot of information that might not be relevant for category inference.
- Before matching material options, extract the key information that could be relevant for material inference. 
- Write the a concise summary of the key information in the "Key Information Summary" field in the required output format.

''',

    # VARIBLE 5: Iterative Self-Refinement
    # Should the LLM give a preliminary answer first, and then evaluate it / improve upon its answer?
    "iterative_self_refinement": '''

**Iterative Self Refinement**
- First, produce an output in the "Preliminary Selection" field.
- Then analyze your own output critically.
- Finally, revise your answer into a final improved version in the "Matched Materials" field.

''',

# ================================
# === PROMPT CONTEXTUALIZATION ===
# ================================

    # VARIABLE 6
    # CONTEXT-AWARE EXAMPLES

    # Anstrichstoffe, Beschichtungen
    "examples_anstrichstoffe": '''
**Matching Example**    
- Material Name in the IFC data says "Anstrich", but has no further constraints, following material options are matched:
"Matched Materials": ["Anstrich, lösemittelverdünnbar, 2 Anstriche", "Anstrich, wasserverdünnbar, 2 Anstriche"]

**True Negative Example**
- Material Name in the IFC data says "Acrylfarbe". There is no match in the "material_options". No material is assigned:
"Matched Materials": []
''',

    # Beton
    "examples_beton": '''
**Example 1: Ambivalent data**
- Material Name in the IFC data says "Ortbeton", and it is a generic load-bearing slab.
- This indicates that EVERY "Hochbaubeton" and "Beton" entry in the "material_options" is assigned, but with a CEM mix 300 or less.

**Example 2: Specific data**
- Material Name indicates that it is screed. This means only a lean concrete mixes are viable.
- In this case, both "Magerbeton" entries from the "material_options" are assigned.
''',

    # Bodenbeläge
    "examples_bodenbelaege": '''
**Example 1: Specific data**
- Material Name says "Laminat". There is only one entry in "material_options" that matches the descriptor.
- Only the entry "Laminat, 8.5 mm" is matched in the output. 

**Example 2: Ambivalent data**
- Material Name in the IFC data says "Natursteinplatte", and there is no indication of how it was processed.
- Then all entries with "Natursteinplatte" are matched.
''',

    # Dichtungsbahnen, Schutzfolien
    "examples_dichtungsbahnen": '''
**Example: Ambivalent data**
- Material Name says "Dichtungsbahn". There are three entries in "material_options" with the word Dichtungsbahn.
- All of those options are matched.
''',

    # Fenster, Sonnenschutz, Fassadenplatten
    "examples_fenster": '''
**Example 1: Ambivalent data**
- The Element "Type" is IfcWindow. There is no indication about glazing and U-value.
- ALL entries with "Isolierverglasung" are matched

**Example 2: Specific data**
- The Element "Type" is IfcWindow. There is an indication that it is triple-glazed and there is a strong emphasis on fire-safety.
- Only the entries with "Isolierverglasung" and an appropriate "Ug-Wert" are matched.
''',

    # Holz und Holzwerkstoffe
    "examples_holz": '''
**Example 1: Ambivalent data**
- The Material Name says "Massivholz". The element's load-bearing pset is True.
- Softwood (Fichte / Tanne / Lärche) are used for structural "Massivholz". All of the softwood entries are matched.

**Example 2: Specific data**
- The Material Name mentions Brettschichtholz. There are only two entries in "material_options" with that descriptor.
- Only those two entries are matched.
''',

    # Klebstoffe Fugendichtungsmassen
    "examples_klebstoffe": "",

    # Kunststoffe
    "examples_kunststoffe": '''
**Example: Specific data**
- The material name says "Plexiglas". The only entry in the "material_options" that matches that name is chosen.
''',

    # Mauersteine
    "examples_mauersteine": '''
**Example 1: Ambivalent data**
- The Material Name says "Leichtzementstein". There are no further specifications in the IFC data.
- All three entries in the "material_options" with the name "Leichtzementstein" are matched.

**Example 2: Specific data**
- The Material Name says "Backstein". But there is no indication of it being insulating. So the "perlitgefüllt" entry in "material_options" is ignored.
- Only the "material_options" entry "Backstein" is matched.
''',

    # Metallbaustoffe
    "examples_metallbaustoffe": '''
**Example 1: Ambivalent data**
- The Element name indicates "Blech". The element is external, so it needs to be resistant to corrosion.
- All "material_options" entries with the name "blech" that are resistant to corrosion are matched.

**Example 2: Specific data**
- The Material Name says "Stahl" and the psets indicate that the element is load-bearing.
- "Stahlprofil, blank" is the only loadbearing entry in "material_options"
''',

    # Mineralische Platten Schüttungen Steine und Ziegel
    "examples_platten": '''
**Example 1: Ambivalent data**
- The Material Name says "Gipsplatte", and the IFC data indicates no further constraints (i.e., usage / function, etc.) 
- There are multiple "material_options" entries with "gips" and "platte" in the name. All of them are matched.

**Example 2: Specific data**
- The Material Name says "Sand". There is only one material options entry with the name "sand" in it.
''',

    # Mörtel und Putze
    "examples_moertel": '''
**Example: Ambivalent data**
- The Material Name says "Putz". The psets indicate that the layer is on the outside.
- All "Putz" entries in "material_options" that are suitable for exterior use are matched.
''',

    # Türen
    "examples_tueren": '''
**Example 1: Ambivalent data**
- The Element Type is IfcDoor, and the psets indicate that it is external. But there is no information about any materials.
- Then we match all of the "Aussentür" entries in the "material_options"

**Example 2: Specific data**
- There is a strong emphasis on fire resistance, and the door is internal.
- The only viable matches are the "Funktionstüren" entries
''',

    # Wärmedämsstoffe
    "examples_waermedaemstoffe": '''
**Example 1: Ambivalent data**
- The Material Descriptor says "Dämmung - Weich". No further constraints. This means we match ALL soft insulation materials
found in the "material_options".

**Example 2: Specific data**
- The material descriptor says "Mineral Wool". There's two types of mineral wool in the "material_options". Steinwolle and Glaswolle.
- For those two, there are multiple entries. All "Steinwolle" and "Glaswolle" "material_options" entries are matched.
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
"Matched Materials": ["<Option 1>", "<Option 2>", ...]
}}
```
If no viable matches are found, return an **empty list** in JSON format: 
```json
{{
"Matched Materials": []
}}
```
''',

    # Output Format extract_then_reason== True
    "output_format_etr": '''
### **Required JSON Output Format:**
**DO NOT** include explanations, commentary, or markdown formatting.
Respond with **valid JSON only**, in the **exact format shown below**:
```json
{{
"Key Information Summary": "<Short summary of Key Information>",
"Matched Materials": ["<Option 1>", "<Option 2>", ...]
}}
```
If no viable matches are found, return an **empty list** in JSON format: 
```json
{{
"Key Information Summary": "<Short summary of Key Information>",
"Matched Materials": []
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
"Preliminary Selection": ["<Option 1>", "<Option 2>", ...],
"Matched Materials": ["<Option 1>", "<Option 2>", ...]
}}
```
If no viable matches are found, return an **empty list** in JSON format: 
```json
{{
"Preliminary Selection": [],
"Matched Materials": []
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
"Preliminary Selection": ["<Option 1>", "<Option 2>", ...],
"Matched Materials": ["<Option 1>", "<Option 2>", ...]
}}
```
If no viable matches are found, return an **empty list** in JSON format: 
```json
{{
"Key Information Summary": "<Short summary of Key Information>",
"Preliminary Selection": [],
"Matched Materials": []
}}
```
'''
}