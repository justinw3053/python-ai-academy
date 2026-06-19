import pytest
from backend.main import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_security_headers(client):
    response = client.get('/api/health')
    assert response.headers.get('Cross-Origin-Opener-Policy') == 'same-origin'
    assert response.headers.get('Cross-Origin-Embedder-Policy') == 'require-corp'

def test_lessons_endpoints(client):
    # Test listing lessons
    response = client.get('/api/lessons')
    assert response.status_code == 200
    lessons_list = response.json
    assert isinstance(lessons_list, list)
    
    if len(lessons_list) > 0:
        # Test getting details for a valid lesson
        first_lesson = lessons_list[0]
        detail_resp = client.get(f"/api/lessons/{first_lesson['id']}")
        assert detail_resp.status_code == 200
        assert "title" in detail_resp.json
        assert "markdown" in detail_resp.json
        assert "exercises" in detail_resp.json

    # Test invalid lesson
    detail_resp = client.get("/api/lessons/invalid_lesson_id")
    assert detail_resp.status_code == 404
