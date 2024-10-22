from application import application as app

class TestEmails:
    def test_health(self):
        with app.test_client() as client:
            response = client.get('/blacklists/ping')
            data = str(response.data)
        assert response.status_code == 200
        assert 'pong' in data