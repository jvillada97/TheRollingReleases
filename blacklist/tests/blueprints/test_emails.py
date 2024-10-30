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

def test_add_without_token(test_client):
    response = test_client.post('/blacklists', json={'email': 'test@example.com'})
    assert response.status_code == 403

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
    
if __name__ == '__main__':
    pytest.main()