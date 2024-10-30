import os
import unittest
from unittest.mock import patch, MagicMock

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

class TestEmails(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_add_without_token(self):
        response = self.client.post('/blacklists', json={'email': 'test@example.com'})
        self.assertEqual(response.status_code, 400)  # Asumiendo 400 por falta de token

    def test_ping(self):
        response = self.client.get('/blacklists/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'pong')

    @patch('blacklist.src.commands.get.GetEmail')
    def test_read_with_token(self, MockGetEmail):
        mock_instance = MockGetEmail.return_value
        mock_instance.execute.return_value = 'Email data'

        response = self.client.get('/blacklists/test@example.com', headers={'Authorization': 'Bearer qwerty'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Email data')

    def test_read_without_token(self):
        response = self.client.get('/blacklists/test@example.com')
        self.assertEqual(response.status_code, 400)  # Asumiendo 400 por falta de token

    def test_health(self):
        response = self.client.get('/blacklists/ping')
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', response.data.decode())

if __name__ == '__main__':
    unittest.main()