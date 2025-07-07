import sys
import os
import pytest

# Add the path to access app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_redirects_to_login(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"login" in response.data.lower()

def test_catalogues_api_get(client):
    response = client.get('/catalogues')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data.get("success") is True
    assert isinstance(data.get("data"), list)

def test_login_success(client):
    response = client.post('/login', json={
        "username": "admin",
        "password": "admin123"
    })
    assert response.status_code in [200, 302]

def test_login_failure(client):
    response = client.post('/login', json={
        "username": "wrong",
        "password": "invalid"
    })
    assert response.status_code == 401
    assert response.get_json().get("success") is False

def test_create_catalogue(client):
    response = client.post('/catalogues', json={
        "catalogue_id": 999,
        "name": "Test Item",
        "description": "Test Desc",
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "is_active": 1
    })
    assert response.status_code in [200, 201]

def test_update_catalogue(client):
    response = client.put('/catalogues/999', json={
        "name": "Updated Test",
        "description": "Updated Desc",
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "is_active": 1
    })
    assert response.status_code in [200, 204]

def test_delete_catalogue(client):
    response = client.delete('/catalogues/999')
    assert response.status_code in [200, 204, 404]

