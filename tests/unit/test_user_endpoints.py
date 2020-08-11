## Something that is untested is broken.
import pytest, os, json, io
from mock import patch

##================ GET USER ================
def test_api_get_user_with_unexisting_id( test_app ):
    response = test_app.get("/api/v1/users/455")
    assert response.status_code == 404 


@patch('novadrive.api.v1.controllers.user_controller.user_manager.get_user_data')
def test_api_get_user_data_correct( mock_user_response, test_app, mocked_user_response):

    #mock get function
    mock_user_response.return_value = json.dumps(mocked_user_response)
    response = test_app.get("/api/v1/users/1")

    assert response.status_code == 200 


##================ GET DRIVE ================
def test_api_get_drive_unexisting_user( test_app ):
    response = test_app.get("/api/v1/users/500/drive")
    assert response.status_code == 404 


@patch('novadrive.api.v1.controllers.user_controller.folder_manager.get_root_folder_content')
def test_api_get_drive_correct( mock_get_drive, test_app, get_folder_content_mocked_result):

    mock_get_drive.return_value = get_folder_content_mocked_result
    response = test_app.get("/api/v1/users/1/drive")

    assert response.status_code == 200 
    assert b"child_folder" in response.data



