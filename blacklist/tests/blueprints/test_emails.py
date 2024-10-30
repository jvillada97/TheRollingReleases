import os
import pytest
from unittest.mock import patch, MagicMock
from blacklist.application import application as app
import uuid

# Mockear variables de entorno antes de importar el módulo application
patch.dict(os.environ, {
    'DB_USER': 'postgres',
    'DB_PASSWORD': 'postgres',
    'DB_HOST': 'localhost',
    'DB_PORT': '5432',
    'DB_NAME': 'postgres',
    'APP_PORT': '3000',
    'TOKEN': 'qwerty'
}).start()

# Mockear la conexión a la base de datos
with patch('blacklist.src.models.models.db.create_all', MagicMock()):
    from blacklist.application import application as app

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

# Test exitosos 
def test_ping(test_client):
    response = test_client.get('/blacklists/ping')
    assert response.status_code == 200
    assert response.data.decode() == 'pong'

def test_add(test_client):
    response = test_client.post('/blacklists', json={'email': 'test@example.com', 'app_uuid': f"{uuid.uuid4()}", 'blocked_reason': 'test'}, headers={'Authorization': 'Bearer qwerty'})
    assert response.status_code == 201

def test_read(test_client):
    response = test_client.get('/blacklists/test@example.com', headers={'Authorization': 'Bearer qwerty'})
    assert response.status_code == 200

# Test error por campos faltantes
def test_add_incomplet(test_client):
    response = test_client.post('/blacklists', json={'email': 'test@example.com', 'blocked_reason': 'test'}, headers={'Authorization': 'Bearer qwerty'})
    assert response.status_code == 400

# Test error por token inválido
def test_add_token_invalid(test_client):
    response = test_client.post('/blacklists', json={'email': 'test@example.com', 'app_uuid': f"{uuid.uuid4()}", 'blocked_reason': 'test'}, headers={'Authorization': 'Bearer 123'})
    assert response.status_code == 401

def test_read_token_invalid(test_client):
    response = test_client.get('/blacklists/test@example.com', headers={'Authorization': 'Bearer 123'})
    assert response.status_code == 401

# Test error por token faltante
def test_read_no_token(test_client):
    response = test_client.get('/blacklists/test@example.com')
    assert response.status_code == 403

def test_add_without_token(test_client):
    response = test_client.post('/blacklists', json={'email': 'test@example.com'})
    assert response.status_code == 403

# Test error por email repetido
def test_add_exist(test_client):
    response = test_client.post('/blacklists', json={'email': 'test@example.com', 'app_uuid': f"{uuid.uuid4()}", 'blocked_reason': 'test'}, headers={'Authorization': 'Bearer qwerty'})
    response = test_client.post('/blacklists', json={'email': 'test@example.com', 'app_uuid': f"{uuid.uuid4()}", 'blocked_reason': 'test'}, headers={'Authorization': 'Bearer qwerty'})
    assert response.status_code == 409

# Test error por información inválida
def test_add_invalid(test_client):
    response = test_client.post('/blacklists', json={'email': 123, 'app_uuid': 123, 'blocked_reason': 123}, headers={'Authorization': 'Bearer qwerty'})
    assert response.status_code == 412

if __name__ == '__main__':
    pytest.main()