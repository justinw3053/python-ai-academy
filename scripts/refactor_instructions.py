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
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "markdown":
            source_lines = cell.get("source", [])
            source_text = "".join(source_lines)
            
            # Keep a copy of original text to check if modified
            original_text = source_text

            # --- GREEK BRIEFING REFACTOR ---
            source_text = source_text.replace(
                "### 1️⃣ Βήμα 1: Ξύπνησε τον Ψηφιακό σου Δάσκαλο (Pi Agent)!\n* Κάνε κλικ στο **δεξί μαύρο παράθυρο** (τερματικό), πληκτρολόγησε τη λέξη:\n  ### `pi`\n  και πάτα **Enter**! \n* Ο προσωπικός σου Socratic δάσκαλος θα ξυπνήσει. Μπορείς να του γράφεις τις ερωτήσεις σου στα Ελληνικά όταν δυσκολεύεσαι!",
                "### 1️⃣ Βήμα 1: Ο Ψηφιακός σου Δάσκαλος (Pi Agent) είναι Έτοιμος!\n* Ο προσωπικός σου Socratic δάσκαλος είναι ήδη συνδεδεμένος και έτοιμος στο δεξί παράθυρο συζήτησης! Μπορείς να του γράφεις τις ερωτήσεις σου στα Ελληνικά όταν δυσκολεύεσαι."
            )
            source_text = source_text.replace(
                "### 3️⃣ Βήμα 3: Ενημέρωσε τον δάσκαλό σου με τη λέξη `πρόοδος`!\n* Μόλις πάρεις πράσινο τσεκάρισμα επιτυχίας σε μια άσκηση, γράψε τη λέξη:\n  ### `πρόοδος`\n  στο δεξί παράθυρο του Pi Agent και πάτα Enter! Θα διαβάσει τη μνήμη σου και θα σε συγχαρεί!",
                "### 3️⃣ Βήμα 3: Ενημέρωσε τον δάσκαλό σου με τη λέξη `progress`!\n* Μόλις πάρεις πράσινο μήνυμα επιτυχίας στην κονσόλα, γράψε τη λέξη **`progress`** στο δεξί παράθυρο συζήτησης του Pi Agent και πάτα Send! Θα ελέγξει τον κώδικά σου και θα σε συγχαρεί!"
            )
            source_text = source_text.replace(
                "### 4️⃣ Βήμα 4: Καθάρισε τη Μνήμη της AI (`/new`)\n* 💡 *AI Tip: Αν ο Pi Agent αρχίσει να καθυστερεί ή να μπερδεύεται επειδή γεμίζει η μνήμη του, γράψε του τη λέξη:* \n  ### `/new` \n  *για να καθαρίσεις τη μνήμη του και να ξαναγίνει ταχύτατος! Κάνε το συνήθεια στην αρχή κάθε μαθήματος.*",
                "### 4️⃣ Βήμα 4: Μάθε χωρίς Όρια!\n* 💡 *AI Tip: Αν ο Pi Agent αρχίσει να μπερδεύεται, μπορείς να του γράψεις **`/new`** στο παράθυρο συζήτησης για να ξεκινήσεις μια νέα καθαρή συζήτηση!*"
            )

            # --- ENGLISH BRIEFING REFACTOR ---
            source_text = source_text.replace(
                "### 1️⃣ Step 1: Wake Up Your Digital Mentor (Pi Agent)!\n* Click on the **right black window** (your terminal), type the word:\n  ### `pi`\n  and hit **Enter**!\n* Your personal Socratic teacher will wake up. You can ask him questions in English whenever you get stuck!",
                "### 1️⃣ Step 1: Your Digital Mentor (Pi Agent) is Ready!\n* Your personal Socratic teacher is already online and waiting in the chat window on the right! You can ask him questions in English whenever you get stuck!"
            )
            source_text = source_text.replace(
                "### 3️⃣ Step 3: Update Your Mentor with the word `progress`!\n* Once you get a green success checkmark on an exercise, type the word:\n  ### `progress`\n  into the Pi Agent's window and hit Enter! He will read your memory files and celebrate your achievement!",
                "### 3️⃣ Step 3: Update Your Mentor with the word `progress`!\n* Once you pass an exercise and see the success message, type the word **`progress`** in the Pi Agent's chat box and click Send! He will check your console code and celebrate your achievement!"
            )
            source_text = source_text.replace(
                "### 4️⃣ Step 4: Clear the AI's Memory (`/new`)\n* 💡 *AI Tip: If the Pi Agent starts lagging or getting confused because his memory is full, type the command:* \n  ### `/new` \n  *to wipe his short-term memory and make him lightning fast again! Make this a habit at the start of every lesson.*",
                "### 4️⃣ Step 4: Learn Without Limits!\n* 💡 *AI Tip: If the Pi Agent starts getting confused or off-topic, just type **`/new`** in the chat window to start a fresh Socratic conversation!*"
            )

            # --- STANDARD TERM REFACTORING ---
            source_text = source_text.replace(
                "Πάτα το κουμπί **Play** ▶️ (στα αριστερά του κουτιού, ή `Ctrl+Enter`) για να τρέξεις το πρόγραμμα",
                "Κάνε κλικ στο πράσινο κουμπί **▶ ΕΚΤΕΛΕΣΗ (RUN CODE)** (στο κάτω μέρος της κονσόλας) για να τρέξεις το πρόγραμμα"
            )
            source_text = source_text.replace("κουμπί **Play** ▶️", "κουμπί **▶ ΕΚΤΕΛΕΣΗ (RUN CODE)**")
            source_text = source_text.replace("κουμπί Play ▶️", "κουμπί **▶ ΕΚΤΕΛΕΣΗ (RUN CODE)**")
            source_text = source_text.replace("κουμπί **Play**", "κουμπί **▶ ΕΚΤΕΛΕΣΗ (RUN CODE)**")
            source_text = source_text.replace("κουμπί Play", "κουμπί **▶ ΕΚΤΕΛΕΣΗ (RUN CODE)**")
            source_text = source_text.replace("κουμπί **play**", "κουμπί **▶ ΕΚΤΕΛΕΣΗ (RUN CODE)**")
            source_text = source_text.replace("κουμπί play", "κουμπί **▶ ΕΚΤΕΛΕΣΗ (RUN CODE)**")
            source_text = source_text.replace("στα αριστερά του κουτιού", "στο κάτω μέρος της κονσόλας")
            source_text = source_text.replace("`Ctrl+Enter`", "κλικ στο RUN CODE")
            source_text = source_text.replace("Ctrl+Enter", "κλικ στο RUN CODE")
            source_text = source_text.replace("στο κελί από κάτω", "στην κονσόλα")
            source_text = source_text.replace("στο κελί παρακάτω", "στην κονσόλα")
            source_text = source_text.replace("δεξί τερματικό", "παράθυρο συζήτησης")
            source_text = source_text.replace("δεξιού τερματικού", "παραθύρου συζήτησης")
            source_text = source_text.replace("δεξί μαύρο παράθυρο", "παράθυρο συζήτησης")
            source_text = source_text.replace("δεξί παράθυρο", "παράθυρο συζήτησης")
            source_text = source_text.replace("δεξιού παραθύρου", "παραθύρου συζήτησης")
            source_text = source_text.replace("κελί", "κονσόλα")
            source_text = source_text.replace("κελιά", "κονσόλα")

            source_text = source_text.replace(
                "Click the **Play** button ▶️ (on the left side of the block, or press `Ctrl+Enter`) to run your program",
                "Click the green **▶ ΕΚΤΕΛΕΣΗ (RUN CODE)** button (at the bottom of the console) to run your program"
            )
            source_text = source_text.replace("on the left side of the block", "at the bottom of the console")
            source_text = source_text.replace("Play button ▶️", "**▶ ΕΚΤΕΛΕΣΗ (RUN CODE)** button")
            source_text = source_text.replace("**Play** button ▶️", "**▶ ΕΚΤΕΛΕΣΗ (RUN CODE)** button")
            source_text = source_text.replace("**Play** button", "**▶ ΕΚΤΕΛΕΣΗ (RUN CODE)** button")
            source_text = source_text.replace("Play button", "**▶ ΕΚΤΕΛΕΣΗ (RUN CODE)** button")
            source_text = source_text.replace("Hit Play!", "Click RUN CODE!")
            source_text = source_text.replace("Hit Play", "Click RUN CODE")
            source_text = source_text.replace("press `Ctrl+Enter`", "click RUN CODE")
            source_text = source_text.replace("press Ctrl+Enter", "click RUN CODE")
            source_text = source_text.replace("in the block below", "in the main console")
            source_text = source_text.replace("in the cell below", "in the main console")
            source_text = source_text.replace("terminal window", "chat window")
            source_text = source_text.replace("terminal", "chat window")
            source_text = source_text.replace("in the side window", "in the chat window")
            source_text = source_text.replace("side window", "chat window")
            source_text = source_text.replace("this cell", "the console")
            source_text = source_text.replace("the cell", "the console")

            if source_text != original_text:
                # Split back into lines to match standard notebook JSON style
                cell["source"] = [line + "\n" for line in source_text.split("\n")]
                # Strip trailing newline of the last element
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
    
    # 1. Refactor root level notebooks
    root_notebooks = glob.glob(os.path.join(base_dir, "*.ipynb"))
    for nb in root_notebooks:
        refactor_notebook(nb)
        
    # 2. Refactor content folder notebooks
    content_notebooks = glob.glob(os.path.join(base_dir, "content", "*.ipynb"))
    for nb in content_notebooks:
        refactor_notebook(nb)

if __name__ == "__main__":
    main()
