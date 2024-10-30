import unittest
from unittest.mock import patch
import pytest

@pytest.mark.usefixtures("test_client")
class TestEmails(unittest.TestCase):
    def setUp(self):
        self.client = self.app.test_client()

    def test_add_without_token(self):
        response = self.client.post('/blacklists', json={'email': 'test@example.com'})
        self.assertEqual(response.status_code, 400)  # Assuming 400 due to missing token

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
        self.assertEqual(response.status_code, 400)  # Assuming 400 due to missing token

    def test_health(self):
        response = self.client.get('/blacklists/ping')
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', response.data.decode())

if __name__ == '__main__':
    unittest.main()