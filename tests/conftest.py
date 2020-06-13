import pytest
import app
import configparser, os
from . import utils

## API TESTING
@pytest.fixture(scope="session", autouse=True)
def test_app():

    test_app = app.create_app( environment = 'TEST' )
    test_app_client = test_app.test_client()

    utils.db_init()

    yield  test_app_client
    
    utils.db_cleanup()
  

@pytest.fixture(scope="module")
def test_user():
    return {'id': 1, 'name': 'test', 'lastname': 'user', 'email': 'angel.pena@gmail.com', 'storage_remaining': "Decimal('10000000')", 'password': '5F4DCC3B5AA765D61D8327DEB882CF99', 'image_uri': None, 'thumbnail_uri': None, 'created': "datetime.datetime(2020, 6, 7, 23, 47, 38)", 'updated': None, 'deleted': None}


@pytest.fixture(scope="module")
def test_folder_object():
    return {'id': 1, 'name': 'testfolder', 'owner_id': 1, 'parent_id': None , 'created': "datetime.datetime(2020, 6, 7, 23, 47, 38)", 'updated': None, 'deleted': None}


@pytest.fixture(scope="module")
def test_file_object():
    return {'id': 1, 'name': 'testfile', 'type':'image/png', 'user_id': 1, 'filesize': 100 , 'file_uri' : 'file/uri/1', 'thumbnail_uri' : 'thumbnail/uri/1', 'folder_id': 1 , 'created': "datetime.datetime(2020, 6, 7, 23, 47, 38)", 'updated': None, 'deleted': None}
