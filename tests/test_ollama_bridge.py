import pytest
from backend.main import create_app
from unittest.mock import patch

@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@patch('backend.llm_bridge.stream_chat')
def test_api_chat_endpoint(mock_stream_chat, client):
    # Mock the generator to yield chunks of SSE data
    def fake_stream():
        yield "data: Hello\n\n"
        yield "data: World\n\n"
        yield "event: done\ndata: \n\n"
    
    mock_stream_chat.return_value = fake_stream()
    
    response = client.post('/api/chat', json={"message": "Help me", "context": "x=5"})
    assert response.status_code == 200
    assert 'text/event-stream' in response.headers['Content-Type']
    
    # Read the streamed response
    data = response.get_data(as_text=True)
    assert "data: Hello" in data
    assert "data: World" in data
