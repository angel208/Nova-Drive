## Something that is untested is broken.
import pytest, os, json, io
from mock import patch

##================ POST FILE ================

def test_api_store_file_with_missing_field_in_json( test_app, post_file_request_data_missing_field ):

    headers= {}
    payload = {'data': json.dumps(post_file_request_data_missing_field) }
   
    response = test_app.post("/api/v1/files/", headers=headers, data = payload)

    assert response.status_code == 400
    assert b"Missing data for required field." in response.data 


def test_api_store_file_with_json_and_no_file( test_app, correct_post_file_request_data ):

    headers= {}
    payload = {'data': json.dumps(correct_post_file_request_data) }
   
    response = test_app.post("/api/v1/files/", headers=headers, data = payload)

    assert response.status_code == 400
    assert b"Bad Request: missing file in request body." in response.data
    


def test_api_store_file_no_json_and_no_file( test_app ):

    response = test_app.post("/api/v1/files/")

    assert response.status_code == 400  
    

@patch('novadrive.api.v1.controllers.file_controller.file_manager.store_file')
def test_api_store_file_correct_payload( mock_store_file, test_app, correct_post_file_request_data, post_file_mocked_result):

    #mock store function
    mock_store_file.return_value = post_file_mocked_result

    #make api call
    payload = {
        'data': json.dumps(correct_post_file_request_data)
    }

    payload['file'] = (io.BytesIO(b"sample text"), 'test.jpg')
   
    response = test_app.post("/api/v1/files/", data = payload  )

    assert response.status_code == 201
    assert str.encode(post_file_mocked_result['file_uri']) in response.data



def test_api_store_file_with_unexisting_folder( test_app, post_file_request_data_unexisting_folder):

    #make api call
    payload = {
        'data': json.dumps(post_file_request_data_unexisting_folder)
    }

    payload['file'] = (io.BytesIO(b"sample text"), 'test.jpg')
   
    response = test_app.post("/api/v1/files/", data = payload  )

    assert response.status_code == 404
    assert b"Folder with given id doesn't exists" in response.data


##================ GET FILE ================  

def test_api_get_file_with_unexisting_id( test_app ):
    response = test_app.get("/api/v1/files/455")
    assert response.status_code == 404 


@patch('novadrive.api.v1.controllers.file_controller.file_manager.get_file_data')
def test_api_get_file_correct( mock_get_file_data, test_app, post_file_mocked_result):

    #mock get function
    mock_get_file_data.return_value = post_file_mocked_result
    response = test_app.get("/api/v1/files/2")

    assert response.status_code == 200 


##================ DELETE FILE ================

def test_api_soft_delete_file_unexisting_file(  test_app ):
    response = test_app.delete("/api/v1/files/500")
    assert response.status_code == 404

@patch('novadrive.api.v1.controllers.file_controller.file_manager.soft_delete_file')
def test_api_soft_delete_file_correct( mock_soft_delete_file, test_app ):

    #mock delete function
    mock_soft_delete_file.return_value = {}

    response = test_app.delete("/api/v1/files/2")

    assert response.status_code == 204



