from unittest.mock import patch
import pytest
import os
import json
from backend.main import create_app

@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_api_track_endpoint(client, tmp_path):
    # Test that the backend endpoint exists and handles progress updates
    test_path = tmp_path / "memory.txt"
    with patch('backend.state_manager.MEMORY_PATH', str(test_path)):
        response = client.post('/api/track', json={"lesson": "Mission 1, Lesson 1"})
        assert response.status_code == 200
        
        # Verify it wrote to disk
        assert os.path.exists(test_path)
        with open(test_path, 'r') as f:
            content = f.read()
            assert "Mission 1, Lesson 1" in content

def test_mock_tracker_in_worker():
    # Test that the worker injects the tracker mock into sys.modules
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    worker_path = os.path.join(base_dir, 'frontend', 'worker.js')
    with open(worker_path, 'r') as f:
        content = f.read()
        
    assert 'sys.modules["tracker"]' in content
    assert 'def update_progress' in content
    assert 'pyodide.http.pyfetch' in content or 'XMLHttpRequest' in content
