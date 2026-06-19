import json
import os

def parse_notebook(filepath):
    """
    Parses a Jupyter Notebook (.ipynb) and extracts markdown instructions,
    starter code, and hidden assertions.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    result = {
        "title": "Unknown Lesson",
        "markdown": "",
        "exercises": []
    }

    markdown_blocks = []

    for cell in notebook.get("cells", []):
        cell_type = cell.get("cell_type")
        source_lines = cell.get("source", [])
        
        if not source_lines:
            continue
            
        source_text = "".join(source_lines)

        if cell_type == "markdown":
            markdown_blocks.append(source_text)
            # Try to extract a title from the first heading
            if source_text.startswith("# ") and result["title"] == "Unknown Lesson":
                result["title"] = source_lines[0].replace("# ", "").strip()

        elif cell_type == "code":
            # Split the code cell at the automated check marker
            separator = "# === AUTOMATED CHECK ==="
            if separator in source_text:
                parts = source_text.split(separator)
                starter_code = parts[0].strip()
                assertions = parts[1].strip() if len(parts) > 1 else ""
            else:
                starter_code = source_text.strip()
                assertions = ""

            result["exercises"].append({
                "starter_code": starter_code,
                "assertions": assertions
            })

    result["markdown"] = "\n\n".join(markdown_blocks)
    return result

def get_lesson_content(lesson_id):
    if not lesson_id.endswith('.ipynb'):
        lesson_id += '.ipynb'
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(base_dir, 'content')
    filepath = os.path.join(content_dir, lesson_id)
    if os.path.exists(filepath):
        return parse_notebook(filepath)
    return None

def list_lessons():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(base_dir, 'content')
    if not os.path.exists(content_dir):
        return []
    
    lessons = []
    # Sort files to maintain curriculum order
    for filename in sorted(os.listdir(content_dir)):
        if filename.endswith('.ipynb') and not filename.endswith('_eng.ipynb'):
            filepath = os.path.join(content_dir, filename)
            try:
                parsed = parse_notebook(filepath)
                lessons.append({
                    "id": filename,
                    "title": parsed["title"]
                })
            except Exception:
                pass
    return lessons
