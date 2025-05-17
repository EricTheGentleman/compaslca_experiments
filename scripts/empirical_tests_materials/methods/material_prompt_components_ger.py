material_prompt_components_ger = {

# ===================================
# === PROMPT REASONING STRATEGIES ===
# ===================================

    # VARIABLE 3: Chain of Thought Reasoning
    # Should the LLM be instructed to think "step-by-step"
    "chain_of_thought": "- Wende eine 'Chain-of-Thought'Begründungsstrategie an. Analysiere alle möglichen Materialoptionen und denke schrittweise, bevor du deine Entscheidung triffst.",

    # VARIABLE 4: Extract-Then-Reason
    # Should the LLM identify and summarize the key information for material inference first?
    "extract_then_reason": '''
**Zuerst Schlüsselinformationen extrahieren**
- In der ersten Eingabe, die die IFC-Daten beschreibt, gibt es viele Informationen, die für die Materialzuodrnung nicht relevant sein könnten.
- Bevor Materialoptionen zugeordnet werden, extrahiere die Schlüsselinformationen, die für die Materialzuordnung relevant sein könnten.
- Schreibe eine kurze Zusammenfassung der Schlüsselinformationen in das Feld "Key Information Summary" im geforderten Ausgabeformat.
''',

    # VARIBLE 5: Iterative Self-Refinement
    # Should the LLM give a preliminary answer first, and then evaluate it / improve upon its answer?
    "iterative_self_refinement": '''
**Iterative Selbstverbesserung**
- Erstelle zuerst eine Ausgabe im Feld "Preliminary Selection".
- Analysiere dann deine eigene Ausgabe kritisch.
- Überarbeite abschließend deine Antwort zu einer verbesserten Endversion im Feld "Matched Materials".
''',

# ================================
# === PROMPT CONTEXTUALIZATION ===
# ================================

    # VARIABLE 6
    # CONTEXT-AWARE EXAMPLES

    # Anstrichstoffe, Beschichtungen
    "examples_anstrichstoffe": '''
**Zuordnungs-Beispiel**    
- Materialname in der IFC-Datei lautet "Anstrich", es gibt jedoch keine weiteren Einschränkungen. Die folgenden Materialoptionen werden zugeordnet:
"Matched Materials": ["Anstrich, lösemittelverdünnbar, 2 Anstriche", "Anstrich, wasserverdünnbar, 2 Anstriche"]

**Negativbeispiel (korrekte Nicht-Zuordnung)**
- Materialname in der IFC-Datei lautet "Acrylfarbe". Es gibt keine Übereinstimmung in den "material_options". Kein Material wird zugeordnet:
"Matched Materials": []
''',

    # Beton
    "examples_beton": '''
**Beispiel 1: Uneindeutige Daten**
- Materialname in der IFC-Datei lautet "Ortbeton", und es handelt sich um eine generische, tragende Decke.
- Dies bedeutet, dass JEDE „Hochbaubeton“- und „Beton“-Eintragung in den "material_options" zugeordnet wird, jedoch nur mit einer CEM-Mischung von 300 oder weniger.

**Beispiel 2: Genaue Daten**
- Der Materialname gibt an, dass es sich um Estrich handelt. Das bedeutet, dass nur magere Betone in Frage kommen.
- In diesem Fall werden beide „Magerbeton“-Einträge aus den "material_options" zugeordnet.
''',

    # Bodenbeläge
    "examples_bodenbelaege": '''
**Beispiel 1: Genaue Daten**
- Der Materialname lautet „Laminat“. Es gibt nur einen Eintrag in den "material_options", der zum Begriff passt.
- Nur der Eintrag „Laminat, 8.5 mm“ wird im Ergebnis zugeordnet.

**Beispiel 2: Uneindeutige Daten**
- Der Materialname in der IFC-Datei lautet „Natursteinplatte“, und es gibt keinen Hinweis darauf, wie sie verarbeitet wurde.
- Dann werden alle Einträge mit „Natursteinplatte“ zugeordnet.
''',

    # Dichtungsbahnen, Schutzfolien
    "examples_dichtungsbahnen": '''
**Beispiel: Uneindeutige Daten**
- Der Materialname lautet „Dichtungsbahn“. Es gibt drei Einträge in den "material_options" mit dem Wort Dichtungsbahn.
- Alle diese Optionen werden zugeordnet.
''',

    # Fenster, Sonnenschutz, Fassadenplatten
    "examples_fenster": '''
**Beispiel 1: Uneindeutige Daten**
- Der Elementtyp ist IfcWindow. Es gibt keine Angaben zur Verglasung oder zum U-Wert.
- ALLE Einträge mit „Isolierverglasung“ werden zugeordnet.

**Beispiel 2: Genaue Daten**
- Der Elementtyp ist IfcWindow. Es wird angegeben, dass es sich um Dreifachverglasung handelt und besonderer Brandschutz erforderlich ist.
- Nur die Einträge mit „Isolierverglasung“ und einem passenden „Ug-Wert“ werden zugeordnet.
''',

    # Holz und Holzwerkstoffe
    "examples_holz": '''
**Beispiel 1: Uneindeutige Daten**
- Der Materialname lautet „Massivholz“. Das Element ist laut Pset tragend.
- Nadelhölzer (Fichte / Tanne / Lärche) werden für tragendes Massivholz verwendet. Alle entsprechenden Nadelholz-Einträge werden zugeordnet.

**Beispiel 2: Genaue Daten**
- Der Materialname nennt „Brettschichtholz“. Es gibt nur zwei Einträge in den "material_options", die diesen Begriff enthalten.
- Nur diese beiden Einträge werden zugeordnet.
''',

    # Klebstoffe Fugendichtungsmassen
    "examples_klebstoffe": "",

    # Kunststoffe
    "examples_kunststoffe": '''
**Beispiel: Genaue Daten**
- Der Materialname lautet „Plexiglas“. Der einzige Eintrag in den "material_options", der diesen Namen enthält, wird ausgewählt.
''',

    # Mauersteine
    "examples_mauersteine": '''
**Beispiel 1: Uneindeutige Daten**
- Der Materialname lautet „Leichtzementstein“. Es gibt keine weiteren Angaben in den IFC-Daten.
- Alle drei Einträge mit dem Namen „Leichtzementstein“ in den "material_options" werden zugeordnet.

**Beispiel 2: Genaue Daten**
- Der Materialname lautet „Backstein“. Es gibt aber keinen Hinweis darauf, dass er dämmend ist. Der „perlitgefüllt“-Eintrag in den "material_options" wird ignoriert.
- Nur der „Backstein“-Eintrag wird zugeordnet.
''',

    # Metallbaustoffe
    "examples_metallbaustoffe": '''
**Beispiel 1: Uneindeutige Daten**
- Der Elementname weist auf „Blech“ hin. Das Element ist außenliegend, daher muss es korrosionsbeständig sein.
- Alle „material_options“-Einträge mit dem Namen „Blech“, die korrosionsbeständig sind, werden zugeordnet.

**Beispiel 2: Genaue Daten**
- Der Materialname lautet „Stahl“ und die Psets zeigen an, dass das Element tragend ist.
- „Stahlprofil, blank“ ist der einzige tragende Eintrag in den "material_options".
''',

    # Mineralische Platten Schüttungen Steine und Ziegel
    "examples_platten": '''
**Beispiel 1: Uneindeutige Daten**
- Der Materialname lautet „Gipsplatte“, und die IFC-Daten enthalten keine weiteren Einschränkungen (z. B. Nutzung / Funktion etc.)
- Es gibt mehrere Einträge in den "material_options", die „Gips“ und „Platte“ im Namen haben. Alle diese werden zugeordnet.

**Beispiel 2: Genaue Daten**
- Der Materialname lautet „Sand“. Es gibt nur einen Eintrag in den "material_options", der „Sand“ im Namen hat.
''',

    # Mörtel und Putze
    "examples_moertel": '''
**Beispiel: Uneindeutige Daten**
- Der Materialname lautet „Putz“. Die Psets geben an, dass die Schicht außen liegt.
- Alle „Putz“-Einträge in den "material_options", die für den Außenbereich geeignet sind, werden zugeordnet.
''',

    # Türen
    "examples_tueren": '''
**Beispiel 1: Uneindeutige Daten**
- Der Elementtyp ist IfcDoor und laut Psets ist die Tür außenliegend. Es gibt jedoch keine Informationen zu verwendeten Materialien.
- Dann werden alle „Aussentür“-Einträge in den "material_options" zugeordnet.

**Beispiel 2: Genaue Daten**
- Es besteht ein besonderer Fokus auf Brandschutz, und die Tür ist innenliegend.
- Nur die „Funktionstüren“-Einträge sind passende Zuordnungen.
''',

    # Wärmedämsstoffe
    "examples_waermedaemstoffe": '''
**Beispiel 1: Uneindeutige Daten**
- Die Materialbeschreibung lautet „Dämmung - Weich“. Keine weiteren Einschränkungen. Das bedeutet, ALLE weichen Dämmstoffe aus den "material_options" werden zugeordnet.

**Beispiel 2: Genaue Daten**
- Die Materialbeschreibung lautet „Mineralwolle“. In den "material_options" gibt es zwei Arten: Steinwolle und Glaswolle.
- Für beide gibt es mehrere Einträge. Alle Einträge mit „Steinwolle“ und „Glaswolle“ in den "material_options" werden zugeordnet.
''',
 
# ======================
# === OUTPUT FORMATS ===
# ======================
# Slightly redundant to write all of them down
# But this is the best workaround with reagards to modular and nested strings

    # Output Format Baseline
    "output_format_baseline": '''
### **Erforderliches JSON-Ausgabeformat:**
**KEINE** zusätzliche Erklärungen, Kommentare, oder Markdown-Formatierungen
Antworte ausschliesslich mit **gültigem JSON**, und zwar **genau im unten gezeigten Format*:
```json
{{
"Matched Materials": ["<Option 1>", "<Option 2>", ...]
}}
```
Wenn keine geeigneten Entsprechungen gefunden werden, gib eine **leere Liste** im JSON-Format zurück:
```json
{{
"Matched Materials": []
}}
```
''',

    # Output Format extract_then_reason== True
    "output_format_etr": '''
### **Erforderliches JSON-Ausgabeformat:**
**KEINE** zusätzliche Erklärungen, Kommentare, oder Markdown-Formatierungen
Antworte ausschliesslich mit **gültigem JSON**, und zwar **genau im unten gezeigten Format*:
```json
{{
"Key Information Summary": "<Kurze Zusammenfassung der Schlüsselinformationen>",
"Matched Materials": ["<Option 1>", "<Option 2>", ...]
}}
```
Wenn keine geeigneten Entsprechungen gefunden werden, gib eine **leere Liste** im JSON-Format zurück:
```json
{{
"Key Information Summary": "<Short summary of Key Information>",
"Matched Materials": []
}}
```
''',

    # Output Format Iterative Self Refinement == True
    "output_format_irs": '''
### **Erforderliches JSON-Ausgabeformat:**
**KEINE** zusätzliche Erklärungen, Kommentare, oder Markdown-Formatierungen
Antworte ausschliesslich mit **gültigem JSON**, und zwar **genau im unten gezeigten Format*:
```json
{{
"Preliminary Selection": ["<Option 1>", "<Option 2>", ...],
"Matched Materials": ["<Option 1>", "<Option 2>", ...]
}}
```
Wenn keine geeigneten Entsprechungen gefunden werden, gib eine **leere Liste** im JSON-Format zurück:
```json
{{
"Preliminary Selection": [],
"Matched Materials": []
}}
```
''',

    # Output Format etr AND isr == True
    "output_format_etr_isr": '''
### **Erforderliches JSON-Ausgabeformat:**
**KEINE** zusätzliche Erklärungen, Kommentare, oder Markdown-Formatierungen
Antworte ausschliesslich mit **gültigem JSON**, und zwar **genau im unten gezeigten Format*:
```json
{{
"Key Information Summary": "<Kurze Zusammenfassung der Schlüsselinformationen>",
"Preliminary Selection": ["<Option 1>", "<Option 2>", ...],
"Matched Materials": ["<Option 1>", "<Option 2>", ...]
}}
```
Wenn keine geeigneten Entsprechungen gefunden werden, gib eine **leere Liste** im JSON-Format zurück:
```json
{{
"Key Information Summary": "<Short summary of Key Information>",
"Preliminary Selection": [],
"Matched Materials": []
}}
```
'''
}