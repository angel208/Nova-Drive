## Something that is untested is broken.
import pytest, os, json, io
from mock import patch

##--------- begin of tests
def test_api_get_user_with_unexisting_id( test_app ):

    response = test_app.get("/api/v1/users/455")

    assert response.status_code == 404 


@patch('novadrive.api.v1.controllers.user_controller.user_manager.get_user_data')
def test_api_get_user_data_correct( mock_user_response, test_app, mocked_user_response):

    #mock store function
    mock_user_response.return_value = json.dumps(mocked_user_response)

    response = test_app.get("/api/v1/users/1")

    assert response.status_code == 200 



