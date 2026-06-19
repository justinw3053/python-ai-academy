import pytest
import os

def test_sync_input_in_worker():
    with open('/Users/justin/python-ai-academy/frontend/worker.js', 'r') as f:
        content = f.read()
    
    # We expect builtins.input to be overridden
    assert 'def custom_input' in content or 'sys.modules["builtins"].input' in content or '__builtins__["input"]' in content
    # We expect the worker to use Atomics.wait
    assert 'Atomics.wait' in content
