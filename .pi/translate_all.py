import os
import json
import glob
import time
from deep_translator import GoogleTranslator

notebooks = [nb for nb in glob.glob("/home/justin/Space_Station_Academy/*.ipynb") if not nb.endswith("_eng.ipynb")]
translator = GoogleTranslator(source='el', target='en')

def translate_text(text):
    if not text.strip():
        return text
    # Avoid translating python syntax tokens or completely english strings
    if all(ord(char) < 128 for char in text):
        return text # mostly english/ascii already
        
    try:
        # Translators can fail on connection issues, adding a tiny sleep
        time.sleep(0.1)
        translated = translator.translate(text)
        return translated if translated else text
    except Exception as e:
        print(f"Translation failed for chunk: {e}")
        return text

for nb_path in notebooks:
    print(f"Translating {os.path.basename(nb_path)}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for cell in data.get('cells', []):
        if cell.get('cell_type') == 'markdown':
            new_source = []
            for line in cell.get('source', []):
                # Translate markdown lines
                translated_line = translate_text(line)
                # Keep original trailing newline if it existed
                if line.endswith('\n') and not translated_line.endswith('\n'):
                    translated_line += '\n'
                new_source.append(translated_line)
            cell['source'] = new_source
            
        elif cell.get('cell_type') == 'code':
            new_source = []
            for line in cell.get('source', []):
                # Only translate python comments and some strings, carefully
                if line.strip().startswith('#'):
                    leading_spaces = len(line) - len(line.lstrip())
                    text_to_translate = line.lstrip()[1:] # remove '#'
                    translated_text = translate_text(text_to_translate)
                    new_line = (' ' * leading_spaces) + '#' + translated_text
                    if line.endswith('\n') and not new_line.endswith('\n'):
                        new_line += '\n'
                    new_source.append(new_line)
                else:
                    # Very simple string translation for print("...") inside Greek text
                    if 'print("' in line and '")' in line:
                        parts = line.split('print("')
                        if len(parts) == 2:
                            text_part = parts[1].split('")')[0]
                            if any(ord(char) > 127 for char in text_part): # has greek
                                translated_text = translate_text(text_part)
                                line = line.replace(f'print("{text_part}")', f'print("{translated_text}")')
                    elif "print('" in line and "')" in line:
                        parts = line.split("print('")
                        if len(parts) == 2:
                            text_part = parts[1].split("')")[0]
                            if any(ord(char) > 127 for char in text_part): # has greek
                                translated_text = translate_text(text_part)
                                line = line.replace(f"print('{text_part}')", f"print('{translated_text}')")
                    elif 'input("' in line and '")' in line:
                        parts = line.split('input("')
                        if len(parts) == 2:
                            text_part = parts[1].split('")')[0]
                            if any(ord(char) > 127 for char in text_part): # has greek
                                translated_text = translate_text(text_part)
                                line = line.replace(f'input("{text_part}")', f'input("{translated_text}")')
                                
                    new_source.append(line)
            cell['source'] = new_source

    base_name = os.path.basename(nb_path)
    name_without_ext = os.path.splitext(base_name)[0]
    new_path = os.path.join(os.path.dirname(nb_path), f"{name_without_ext}_eng.ipynb")
    
    with open(new_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
print("All notebooks translated to English!")