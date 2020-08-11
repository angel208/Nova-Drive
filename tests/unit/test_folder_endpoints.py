## Something that is untested is broken.
import pytest, os, json, io
from mock import patch

##--------- begin of tests

def test_api_store_folder_with_missing_field_in_json( test_app, post_folder_request_data_missing_field ):

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    payload =  json.dumps(post_folder_request_data_missing_field) 
   
    response = test_app.post("/api/v1/folders/", headers=headers, data = payload)

    assert response.status_code == 400
    assert b"Missing data for required field." in response.data 
  

@patch('novadrive.api.v1.controllers.folder_controller.folder_manager.create_folder')
def test_api_store_folder_correct_payload( mock_store_folder, test_app, correct_post_folder_request_data, post_folder_mocked_result):

    #mock store function
    mock_store_folder.return_value = post_folder_mocked_result

    #make api call
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    payload =  json.dumps(correct_post_folder_request_data)
 
    response = test_app.post("/api/v1/folders/", headers=headers, data = payload  )

    assert response.status_code == 201
    assert str.encode(post_folder_mocked_result['name']) in response.data



def test_api_store_folder_with_unexisting_parent( test_app, post_folder_request_data_unexisting_parent):

    #make api call
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    payload = json.dumps(post_folder_request_data_unexisting_parent)
  
    response = test_app.post("/api/v1/folders/", headers=headers, data = payload  )

    assert response.status_code == 404
    assert b"Folder with given id doesn't exists" in response.data


  
def test_api_get_folder_data_with_unexisting_id( test_app ):

    response = test_app.get("/api/v1/folders/455")

    assert response.status_code == 404 


@patch('novadrive.api.v1.controllers.folder_controller.folder_manager.get_folder_data')
def test_api_get_folder_data_correct( mock_get_folder_data, test_app, post_folder_mocked_result):

    #mock store function
    mock_get_folder_data.return_value = json.dumps(post_folder_mocked_result)

    response = test_app.get("/api/v1/folders/2")

    assert response.status_code == 200 



