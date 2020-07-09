## Something that is untested is broken.
import pytest, os, json, io
from mock import patch

##--------- begin of tests

def test_api_file_with_missing_field_in_json( test_app, post_file_request_data_missing_field ):

    headers= {}
    payload = {'data': json.dumps(post_file_request_data_missing_field) }
   
    response = test_app.post("/api/v1/files/", headers=headers, data = payload)

    assert response.status_code == 400
    assert b"Missing data for required field." in response.data 


def test_api_file_with_json_and_no_file( test_app, correct_post_file_request_data ):

    headers= {}
    payload = {'data': json.dumps(correct_post_file_request_data) }
   
    response = test_app.post("/api/v1/files/", headers=headers, data = payload)

    assert response.status_code == 400
    assert b"Bad Request: missing file in request body." in response.data
    


def test_api_file_no_json_and_no_file( test_app ):

    response = test_app.post("/api/v1/files/")

    assert response.status_code == 400  
    

@patch('novadrive.api.v1.controllers.files_controller.file_manager.store_file')
def test_api_file_correct_payload( mock_store_file, test_app, correct_post_file_request_data, post_file_mocked_result):

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



def test_api_file_with_unexisting_folder( test_app, post_file_request_data_unexisting_folder):

    #make api call
    payload = {
        'data': json.dumps(post_file_request_data_unexisting_folder)
    }

    payload['file'] = (io.BytesIO(b"sample text"), 'test.jpg')
   
    response = test_app.post("/api/v1/files/", data = payload  )

    assert response.status_code == 404
    assert b"Folder with given id doesn't exists" in response.data


