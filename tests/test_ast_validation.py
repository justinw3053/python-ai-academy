import pytest
import os

def test_ast_validation_in_worker():
    with open('/Users/justin/python-ai-academy/frontend/worker.js', 'r') as f:
        content = f.read()
    
    # We expect an ast validation function to be defined
    assert 'import ast' in content
    assert 'def validate_ast' in content
    # We expect it to be called before exec
    assert 'validate_ast(js_code' in content
