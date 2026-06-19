import pytest
import threading
import time
import requests
from backend.main import create_app
import webview
from unittest.mock import patch, MagicMock
from app import start_server, wait_for_server

# Mock the actual webview.start to prevent popping windows during tests
@patch('webview.create_window')
@patch('webview.start')
def test_app_startup_sync(mock_start, mock_create_window):
    # This tests the wait_for_server logic
    app = create_app()
    
    server_thread = threading.Thread(target=lambda: app.run(port=5001, use_reloader=False))
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for the server to be healthy
    assert wait_for_server('http://127.0.0.1:5001/api/health', timeout=5) == True
    
    # Verify we can make a request
    resp = requests.get('http://127.0.0.1:5001/api/health')
    assert resp.status_code == 200
