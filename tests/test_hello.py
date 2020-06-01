## Something that is untested is broken.
import pytest

from novadrive import nova

@pytest.fixture
def client():
    app = nova.flask_app
    client = app.test_client()
    return client


##--------- begin of tests

def test_hello(client):

    response = client.get("/api/v1/")
    assert response.status_code == 200
    assert b'Welcome to Nova Drive!' in response.data