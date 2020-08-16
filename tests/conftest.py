import pytest
import app
import configparser, os
from . import utils

##================ API REST TESTING FIXTURE ================

@pytest.fixture(scope="session", autouse=True)
def test_app():

    test_app = app.create_app( environment = 'TEST' )
    test_app_client = test_app.test_client()

    utils.db_init()

    yield  test_app_client
    
    utils.db_cleanup()
  
##================ DB INTEGRATION TESTING FIXTURES ================

@pytest.fixture(scope="module")
def test_user():
    return {'id': 1, 'name': 'test', 'lastname': 'user', 'email': 'angel.pena@gmail.com', 'storage_remaining': "Decimal('10000000')", 'password': '5F4DCC3B5AA765D61D8327DEB882CF99', 'image_uri': None, 'thumbnail_uri': None, 'created': "datetime.datetime(2020, 6, 7, 23, 47, 38)", 'updated': None, 'deleted': None}

@pytest.fixture(scope="module")
def test_folder_object():
    return {'id': 1, 'name': 'testfolder', 'owner_id': 1, 'parent_id': None , 'created': "datetime.datetime(2020, 6, 7, 23, 47, 38)", 'updated': None, 'deleted': None}

@pytest.fixture(scope="module")
def test_folder_object_2():
    return {'id': 3, 'name': 'childfolder', 'owner_id': 1, 'parent_id': 1 , 'created': "datetime.datetime(2020, 6, 7, 23, 47, 38)", 'updated': None, 'deleted': None}

@pytest.fixture(scope="module")
def test_file_object():
    return {'id': 1, 'name': 'testfile', 'type':'image/png', 'user_id': 1, 'filesize': 100 , 'file_uri' : 'file/uri/1', 'thumbnail_uri' : 'thumbnail/uri/1', 'folder_id': 1 , 'created': "datetime.datetime(2020, 6, 7, 23, 47, 38)", 'updated': None, 'deleted': None}


##================ MARSHMALLOW VALIDATION FIXTURE ================

@pytest.fixture()
def test_marshmallow_validation_errors():
    
    errors = [

        {},
        {'namex': ['Unknown field.'], 'asd': ['Unknown field.']},
        {'name': ['Missing data for required field.'], 'namex': ['Unknown field.'], 'asd': ['Unknown field.']}

    ]

    return errors

##================ FILE ENDPOINT TESTING FIXTURE ================

@pytest.fixture()
def correct_post_file_request_data():
    return {"name":"asd",
            "type" : "1",
            "folder_id":"1",
            "asd":"asd"}

@pytest.fixture()
def post_file_mocked_result():
    return {
            "id": 28,
            "name": "asd",
            "folder_id": 1,
            "type": "text/plain",
            "filesize": 190,
            "user_id": 1,
            "file_uri": "/api/v1/files/28/download/asd",
            "thumbnail_uri": ""
        }


@pytest.fixture()
def correct_post_file_response():

    return { "id": 28, "name": "asd", "folder_id": 1, "type": "text/plain", "filesize": 190,  "user_id": 1, "file_uri": "/api/v1/files/28/download/asd", "thumbnail_uri": "",  "created": "2020-07-09T03:20:26", "updated": null, "deleted": null }

@pytest.fixture()
def post_file_request_data_missing_field():
    return {"type" : "1",
            "folder_id":"1",
            "asd":"asd"}

@pytest.fixture()
def post_file_request_data_unexisting_folder():
    return {"name":"asd",
            "type" : "1",
            "folder_id":"1000",
            "asd":"asd"}


##================ FOLDER ENDPOINT TESTING FIXTURE ================


@pytest.fixture()
def correct_post_folder_request_data():
    return { 
        "name": "asd",
        "parent_id": "12",
        "asd": "ad"
    }


@pytest.fixture()
def post_folder_mocked_result():
    return {
            "id": 34,
            "name": "mocked folder name",
            "parent_id": 12,
            "owner_id": 1
        }

@pytest.fixture()
def correct_post_folder_response():
    return {
        "id": 34,
        "name": "asd",
        "parent_id": 12,
        "owner_id": 1
    }

@pytest.fixture()
def post_folder_request_data_missing_field():
    return {
        "parent_id": "12",
	    "asd": "ad"
    }

@pytest.fixture()
def post_folder_request_data_unexisting_parent():
    return {
        "name": "asd",
        "parent_id": "120",
        "asd": "ad"
    }

@pytest.fixture()
def get_folder_content_mocked_result():
    return {
            "id": 1,
            "name": "folder1",
            "parent_id": None,
            "owner_id": 1,
            "files": [
                {
                "id": 1,
                "name": "file 1",
                "folder_id": 1,
                "type": "sad",
                "filesize": 123,
                "user_id": 1,
                "file_uri": "asdasd",
                "thumbnail_uri": "asdasda",
                }
            ],
            "folders": [
                {
                "id": 2,
                "name": "child_folder",
                "parent_id": 1,
                "owner_id": 1,
                }
            ]
    }

##================ USER ENDPOINT TESTING FIXTURE ================

@pytest.fixture()
def mocked_user_response():
    return {
        "id": 1,
        "name": "angel",
        "email": "angel@gmail.com",
        "root_folder_id": 1
    }

@pytest.fixture()
def correct_user_response():
    return {
        "id": 1,
        "name": "angel",
        "email": "angel@gmail.com",
        "root_folder_id": 1
    }
