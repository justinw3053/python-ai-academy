import pytest
import os

def test_pyodide_worker_exists():
    assert os.path.exists('/Users/justin/python-ai-academy/frontend/worker.js')
    
    with open('/Users/justin/python-ai-academy/frontend/worker.js', 'r') as f:
        content = f.read()
        
    assert 'importScripts(\'./pyodide/pyodide.js\')' in content
    assert 'self.pyodide.runPythonAsync' in content
    assert 'CustomStdout' in content
    assert '_student_globals.clear()' in content
    assert 'exec(js_student_code, _student_globals)' in content
