import os
import sys
import threading
from datetime import datetime

# Dynamically resolve memory path to the .pi/memory.txt file in the workspace
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_PATH = os.path.join(BASE_DIR, '.pi', 'memory.txt')
_lock = threading.Lock()

def _ensure_dir():
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)

def update_progress(lesson_name):
    with _lock:
        _ensure_dir()
        
        # Only use the tracker.py logic if MEMORY_PATH is the default .pi/memory.txt
        default_path = os.path.join(BASE_DIR, '.pi', 'memory.txt')
        if MEMORY_PATH == default_path:
            pi_path = os.path.join(BASE_DIR, '.pi')
            if pi_path not in sys.path:
                sys.path.append(pi_path)
                
            try:
                import tracker
                tracker.update_progress(lesson_name)
                return True
            except Exception:
                pass
                
        # Fallback/Testing block if tracker is not used or MEMORY_PATH is customized
        content = ""
        if os.path.exists(MEMORY_PATH):
            with open(MEMORY_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
                
        if lesson_name not in content:
            with open(MEMORY_PATH, 'a', encoding='utf-8') as f:
                f.write(f"\nCompleted: {lesson_name} at {datetime.now().isoformat()}")
        return True
