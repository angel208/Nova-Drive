## Something that is untested is broken.
import pytest, os, json, io
from mock import patch

##================ POST FOLDER ================

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


##================ GET FOLDER ================
  
def test_api_get_folder_data_with_unexisting_id( test_app ):
    response = test_app.get("/api/v1/folders/455")
    assert response.status_code == 404 


@patch('novadrive.api.v1.controllers.folder_controller.folder_manager.get_folder_data')
def test_api_get_folder_data_correct( mock_get_folder_data, test_app, post_folder_mocked_result):

    #mock get function
    mock_get_folder_data.return_value = post_folder_mocked_result
    response = test_app.get("/api/v1/folders/2")

    assert response.status_code == 200
    assert b"mocked folder name" in response.data 



##================ GET FOLDER CONTENT ================

def test_api_get_folder_content_with_unexisting_id( test_app ):
    response = test_app.get("/api/v1/folders/455/files")
    assert response.status_code == 404 


@patch('novadrive.api.v1.controllers.folder_controller.folder_manager.get_folder_content')
def test_api_get_folder_content_correct( mock_get_folder_content, test_app, get_folder_content_mocked_result):

    #mock get function
    mock_get_folder_content.return_value = get_folder_content_mocked_result
    response = test_app.get("/api/v1/folders/2/files")

    assert response.status_code == 200 
    assert b"child_folder" in response.data

##================ DELETE FOLDER ================

def test_api_soft_delete_folder_unexisting_folder( test_app ):
    response = test_app.delete("/api/v1/folders/500")
    assert response.status_code == 404


@patch('novadrive.api.v1.controllers.folder_controller.folder_manager.soft_delete_folder')
def test_api_soft_delete_folder_correct( mock_soft_delete_folder, test_app ):

    #mock delete function
    mock_soft_delete_folder.return_value = {}
    response = test_app.delete("/api/v1/folders/2")

    assert response.status_code == 204