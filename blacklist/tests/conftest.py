import pytest
from dotenv import load_dotenv, find_dotenv
from blacklist.application import application as app, db
import os

def pytest_configure(config):
    env_file = find_dotenv('../.env.test')
    load_dotenv(env_file)
    print(f"Loaded environment variables from {env_file}")
    print(f"DB_USER: {os.getenv('DB_USER')}")
    print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
    print(f"DB_HOST: {os.getenv('DB_HOST')}")
    print(f"DB_PORT: {os.getenv('DB_PORT')}")
    print(f"DB_NAME: {os.getenv('DB_NAME')}")
    print(f"APP_PORT: {os.getenv('APP_PORT')}")

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    with app.app_context():
        db.create_all()
        testing_client = app.test_client()
        yield testing_client
        db.drop_all()

@pytest.fixture(autouse=True)
def cleanup(test_client):
    with test_client.application.app_context():
        yield
        with db.session.begin(subtransactions=True):
            db.session.remove()
            db.drop_all()
            db.create_all()