import os
import json

def update_progress(lesson_id):
    try:
        memory_path = "/home/justin/Space_Station_Academy/.pi/memory.txt"
        if not os.path.exists(memory_path):
            return
            
        with open(memory_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        updated_lines = []
        for line in lines:
            # Check for English and legacy Greek keywords
            if line.startswith("COMPLETED WORKBOOKS:") or line.startswith("ΟΛΟΚΛΗΡΩΜΕΝΑ WORKBOOKS:"):
                # Extract completed list
                parts = line.split(":", 1)
                list_str = parts[1].strip()
                if list_str == "[]" or not list_str:
                    completed_list = []
                else:
                    try:
                        # Clean Python list formatting to parse as JSON
                        clean_str = list_str.replace("'", '"')
                        completed_list = json.loads(clean_str)
                    except Exception:
                        completed_list = []
                        
                if lesson_id not in completed_list:
                    completed_list.append(lesson_id)
                updated_lines.append(f"COMPLETED WORKBOOKS: {completed_list}\n")
                
            elif line.startswith("CURRENT WORKBOOK:") or line.startswith("ΤΡΕΧΟΝ WORKBOOK:"):
                # Set the current active lesson/task dynamically
                updated_lines.append(f"CURRENT WORKBOOK: {lesson_id}\n")
            else:
                updated_lines.append(line)
                
        with open(memory_path, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)
            
    except Exception as e:
        # Silently fail inside Jupyter cells to prevent disturbing execution
        pass