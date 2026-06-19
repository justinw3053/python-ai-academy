#!/usr/bin/env python3
import os
import json
import glob

def refactor_notebook(filepath):
    print(f"Refactoring {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            notebook = json.load(f)
        except Exception as e:
            print(f"Failed to parse JSON in {filepath}: {e}")
            return

    modified = False
    is_eng = filepath.endswith("_eng.ipynb")

    for cell in notebook.get("cells", []):
        cell_type = cell.get("cell_type")
        source_lines = cell.get("source", [])
        source_text = "".join(source_lines)
        original_text = source_text

        if cell_type == "markdown":
            # 1. Remove VS Code / Jupyter / Kernel troubleshooting bullet points
            source_text = source_text.replace(
                "* **Αν σου ζητήσει \"Select Kernel\" ή \"Επιλογή Kernel\" (πάνω δεξιά):** Κάνε κλικ εκεί, διάλεξε **'Python Environments...'** και μετά διάλεξε την έκδοση της Python που σου προτείνει (π.χ. 'Python 3.x').\n", ""
            )
            source_text = source_text.replace(
                "* **Αν σου ζητήσει εγκατάσταση 'Python' / 'Jupyter' extension:** Πάτα το κουμπί **Install (Εγκατάσταση)** και περίμενε μερικά δευτερόλεπτα!\n", ""
            )
            source_text = source_text.replace(
                "* **If it asks you to \"Select Kernel\" (top right):** Click it, select **'Python Environments...'**, and choose the recommended Python version (e.g., 'Python 3.x').\n", ""
            )
            source_text = source_text.replace(
                "* **If it asks you to install the 'Python' / 'Jupyter' extension:** Click **Install** and wait a few seconds!\n", ""
            )
            source_text = source_text.replace(
                "* **Αν κολλήσει ο κώδικας και δεν τρέχει τίποτα:** Πάτα το κυκλικό βελάκι **Restart (Επανεκκίνηση)** στο πάνω μέρος του παραθύρου.\n",
                "* **Αν κολλήσει ο κώδικας και δεν τρέχει τίποτα (π.χ. σε ατέρμονη λούπα):** Μην ανησυχείς! Απλά κλείσε και ξανανοίξε την εφαρμογή Space Station Academy για να κάνεις επανεκκίνηση στον πυρήνα!\n"
            )
            source_text = source_text.replace(
                "* **If the code gets stuck and won't run:** Click the circular **Restart** arrow at the top of the window.\n",
                "* **If the code gets stuck and won't run (e.g., in an infinite loop):** Don't worry! Just close and relaunch the Space Station Academy application to restart the core!\n"
            )

            # 2. Refactor Workbook -> Mission / Chapter
            if is_eng:
                # English replacements
                source_text = source_text.replace("# Workbook 1:", "# Mission 1:")
                source_text = source_text.replace("# Workbook 1B:", "# Mission 1B:")
                source_text = source_text.replace("# Workbook 2:", "# Mission 2:")
                source_text = source_text.replace("# Workbook 3:", "# Mission 3:")
                source_text = source_text.replace("# Workbook 4:", "# Mission 4:")
                source_text = source_text.replace("# Workbook 5:", "# Mission 5:")
                source_text = source_text.replace("# Workbook 6:", "# Mission 6:")
                source_text = source_text.replace("# Workbook 7:", "# Mission 7:")
                source_text = source_text.replace("# Workbook 8:", "# Mission 8:")
                source_text = source_text.replace("# Workbook 9:", "# Mission 9:")
                
                source_text = source_text.replace("Welcome to your second workbook!", "Welcome to your second mission!")
                source_text = source_text.replace("Welcome to your very first interactive workbook (Jupyter Notebook)!", "Welcome to your very first interactive programming mission!")
                source_text = source_text.replace("interactive workbook (Jupyter Notebook)", "interactive mission")
                source_text = source_text.replace("interactive workbook", "interactive mission")
                source_text = source_text.replace("Jupyter Workbook", "Mission Card")
                source_text = source_text.replace("Jupyter Notebook", "Mission Card")
                source_text = source_text.replace("Workbook", "Mission")
                source_text = source_text.replace("workbook", "mission")
            else:
                # Greek replacements
                source_text = source_text.replace("# Workbook 1:", "# Αποστολή 1:")
                source_text = source_text.replace("# Workbook 1B:", "# Αποστολή 1Β:")
                source_text = source_text.replace("# Workbook 2:", "# Αποστολή 2:")
                source_text = source_text.replace("# Workbook 3:", "# Αποστολή 3:")
                source_text = source_text.replace("# Workbook 4:", "# Αποστολή 4:")
                source_text = source_text.replace("# Workbook 5:", "# Αποστολή 5:")
                source_text = source_text.replace("# Workbook 6:", "# Αποστολή 6:")
                source_text = source_text.replace("# Workbook 7:", "# Αποστολή 7:")
                source_text = source_text.replace("# Workbook 8:", "# Αποστολή 8:")
                source_text = source_text.replace("# Workbook 9:", "# Αποστολή 9:")
                
                source_text = source_text.replace("Καλώς όρισες στο πρώτο σου διαδραστικό τετράδιο εργασίας (Jupyter Workbook)!", "Καλώς όρισες στην πρώτη σου διαδραστική αποστολή προγραμματισμού!")
                source_text = source_text.replace("πρώτο σου διαδραστικό τετράδιο εργασίας για την AI (AI Workbook)!", "πρώτη σου διαδραστική αποστολή για την AI!")
                source_text = source_text.replace("τετράδιο εργασίας (Jupyter Workbook)", "διαδραστική αποστολή")
                source_text = source_text.replace("τετράδιο εργασίας", "αποστολή")
                source_text = source_text.replace("τετράδια εργασίας", "αποστολές")
                source_text = source_text.replace("Jupyter Workbook", "Αποστολή")
                source_text = source_text.replace("Jupyter Notebook", "Αποστολή")
                source_text = source_text.replace("Workbook", "Αποστολή")
                source_text = source_text.replace("workbook", "αποστολή")

        elif cell_type == "code":
            # 3. Refactor progress logging code strings
            source_text = source_text.replace('update_progress("Workbook ', 'update_progress("Mission ')
            source_text = source_text.replace('update_progress("Workbook 1,', 'update_progress("Mission 1,')
            source_text = source_text.replace('update_progress("Workbook 2,', 'update_progress("Mission 2,')
            source_text = source_text.replace('update_progress("Workbook 3,', 'update_progress("Mission 3,')
            source_text = source_text.replace('update_progress("Workbook 4,', 'update_progress("Mission 4,')
            source_text = source_text.replace('update_progress("Workbook 5,', 'update_progress("Mission 5,')
            source_text = source_text.replace('update_progress("Workbook 6,', 'update_progress("Mission 6,')
            source_text = source_text.replace('update_progress("Workbook 7,', 'update_progress("Mission 7,')
            source_text = source_text.replace('update_progress("Workbook 8,', 'update_progress("Mission 8,')
            source_text = source_text.replace('update_progress("Workbook 9,', 'update_progress("Mission 9,')

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
    
    # Update both root notebooks and content folder notebooks
    for folder in [base_dir, os.path.join(base_dir, "content")]:
        notebooks = glob.glob(os.path.join(folder, "*.ipynb"))
        for nb in notebooks:
            refactor_notebook(nb)

if __name__ == "__main__":
    main()
