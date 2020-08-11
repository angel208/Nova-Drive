## Something that is untested is broken.
import pytest

##================ SAMPLE API TEST ================
def test_hello(test_app):

    response = test_app.get("/api/v1/")
    assert response.status_code == 200
    assert b'Welcome to Nova Drive!' in response.data

