import os
import threading
from datetime import datetime

# In production this would be ~/.local/share/Space_Station_Academy/memory.txt
# For testing we use a local tmp dir if not overridden
MEMORY_PATH = os.path.expanduser("~/.config/space-station-academy/memory.txt")
_lock = threading.Lock()

def _ensure_dir():
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)

def update_progress(lesson_name):
    with _lock:
        _ensure_dir()
        
        # Read current memory
        content = ""
        if os.path.exists(MEMORY_PATH):
            with open(MEMORY_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
                
        # Super simple mock update for now
        if lesson_name not in content:
            with open(MEMORY_PATH, 'a', encoding='utf-8') as f:
                f.write(f"\nCompleted: {lesson_name} at {datetime.now().isoformat()}")
        
        return True
