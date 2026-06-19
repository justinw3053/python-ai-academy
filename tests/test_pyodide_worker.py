import pytest
import os

def test_pyodide_worker_exists():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    worker_path = os.path.join(base_dir, 'frontend', 'worker.js')
    assert os.path.exists(worker_path)
    
    with open(worker_path, 'r') as f:
        content = f.read()
        
    assert 'importScripts(\'./pyodide/pyodide.js\')' in content
    assert 'self.pyodide.runPythonAsync' in content
    assert 'CustomStdout' in content
    assert '_student_globals.clear()' in content
    assert 'exec(js_code, _student_globals)' in content
