import pytest
import os

def test_sync_input_in_worker():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    worker_path = os.path.join(base_dir, 'frontend', 'worker.js')
    with open(worker_path, 'r') as f:
        content = f.read()
    
    # We expect builtins.input to be overridden
    assert 'def custom_input' in content or 'sys.modules["builtins"].input' in content or '__builtins__["input"]' in content
    # We expect the worker to use Atomics.wait
    assert 'Atomics.wait' in content
