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
