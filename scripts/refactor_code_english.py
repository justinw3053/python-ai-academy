#!/usr/bin/env python3
import os
import json
import glob

def refactor_notebook_variables(filepath):
    print(f"Refactoring variables in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            notebook = json.load(f)
        except Exception as e:
            print(f"Failed to parse JSON in {filepath}: {e}")
            return

    modified = False
    
    # Complete mapping of Greeklish variables to professional English variables
    replacements = {
        # General/System variables
        "onoma_skafous": "ship_name",
        "synoliki_energeia": "total_energy",
        "aspides": "shields",
        "taxytita": "speed",
        "thermokrasia_float": "float_temperature",
        "thermokrasia_akeraia": "int_temperature",
        "thermokrasia": "temperature",
        "oxygono": "oxygen_level",
        "epipedo_antirypansis": "pollution_level",
        "onoma_hristh": "user_name",
        "onoma": "name",
        "eilikia": "age",
        "apantisi": "response",
        "lista_stoixeiwn": "element_list",
        "lista_systhmatwn": "system_list",
        "lista": "item_list",
        "pinakas": "diagnostics_grid",
        "vathmos": "grade",
        "epipedo": "level",
        "anagnoristiko": "id",
        "xronos": "time_seconds",
        "aerio": "gas_type",
        "piesi": "pressure",
        "fortio": "cargo_load",
        
        # Hardcoded paths
        "/home/justin/Space_Station_Academy/.pi": "/opt/space-station-academy/.pi"
    }

    for cell in notebook.get("cells", []):
        cell_type = cell.get("cell_type")
        source_lines = cell.get("source", [])
        source_text = "".join(source_lines)
        original_text = source_text

        # Run variable replacements
        for greeklish, english in replacements.items():
            source_text = source_text.replace(greeklish, english)

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
            refactor_notebook_variables(nb)

if __name__ == "__main__":
    main()
