import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    resp = client.get('/api/health')
    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'ok'


def test_message(client):
    resp = client.get('/api/message')
    assert resp.status_code == 200
    assert 'message' in resp.get_json()
