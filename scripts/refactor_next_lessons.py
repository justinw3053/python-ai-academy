#!/usr/bin/env python3
import os
import json
import glob
import re

def refactor_notebook(filepath):
    print(f"Refactoring {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            notebook = json.load(f)
        except Exception as e:
            print(f"Failed to parse JSON: {e}")
            return

    modified = False
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "markdown":
            source_lines = cell.get("source", [])
            source_text = "".join(source_lines)
            original_text = source_text

            # Greek next lesson references (e.g. "Κλείσε αυτό το τετράδιο και άνοιξε το **`01B_Comms_Systems.ipynb`**")
            source_text = re.sub(
                r"[Κκ]λείσε αυτό το τετράδιο και άνοιξε το \*\*`[\w_]+\.ipynb`\*\*",
                "Κάνε κλικ στο κουμπί **ΕΠΟΜΕΝΟ ΜΑΘΗΜΑ (NEXT)**",
                source_text
            )
            source_text = re.sub(
                r"[ΑαΆά]νοιξε το \*\*`[\w_]+\.ipynb`\*\*",
                "Κάνε κλικ στο κουμπί **ΕΠΟΜΕΝΟ ΜΑΘΗΜΑ (NEXT)**",
                source_text
            )
            
            # English next lesson references (e.g. "Close this notebook and open **`01B_Comms_Systems_eng.ipynb`**")
            source_text = re.sub(
                r"[Cc]lose this notebook and open \*\*`[\w_]+\.ipynb`\*\*",
                "Click the **NEXT MISSION (NEXT)** button",
                source_text
            )
            source_text = re.sub(
                r"[Oo]pen \*\*`[\w_]+\.ipynb`\*\*",
                "Click the **NEXT MISSION (NEXT)** button",
                source_text
            )

            if source_text != original_text:
                cell["source"] = [line + "\n" for line in source_text.split("\n")]
                if cell["source"] and cell["source"][-1] == "\n":
                    cell["source"].pop()
                if cell["source"]:
                    cell["source"][-1] = cell["source"][-1].rstrip("\n")
                modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        print(f"Successfully refactored {filepath}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for folder in [base_dir, os.path.join(base_dir, "content")]:
        notebooks = glob.glob(os.path.join(folder, "*.ipynb"))
        for nb in notebooks:
            refactor_notebook(nb)

if __name__ == "__main__":
    main()
