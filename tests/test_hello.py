## Something that is untested is broken.
import pytest

import app

@pytest.fixture
def client():
    test_app = app.flask_app
    client = test_app.test_client()
    return client


##--------- begin of tests

def test_hello(client):

    response = client.get("/api/v1/")
    assert response.status_code == 200
    assert b'Welcome to Nova Drive!' in response.data