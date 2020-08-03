## Something that is untested is broken.
import pytest
from operator import itemgetter
from mysql.connector import errors as mysqlErrors

from novadrive.api.v1.database import user as user_module
from novadrive.api.v1.database import folder as folder_module
from novadrive.api.v1.database import file as file_module

from novadrive.api.v1.utils.errors import ForeignResourceNotFoundException, ResourceNotFoundException

##--------- users

def test_get_user(test_user):

    user = user_module.get_user( id = 1 )
    assert user['name'] == test_user['name']

#----------folders

def test_create_folder(test_folder_object):

    name, parent_id, owner_id = itemgetter('name', 'parent_id', 'owner_id')(test_folder_object)

    folder_id = folder_module.store_folder_in_db( name, parent_id, owner_id )

    assert folder_id == 1


def test_create_folder_unexisting_parent_key(test_folder_object):

    name, parent_id, owner_id = itemgetter('name', 'parent_id', 'owner_id')(test_folder_object)
    parent_id = 24

    with pytest.raises( ForeignResourceNotFoundException ):
       assert folder_module.store_folder_in_db( name, parent_id, owner_id )

def test_get_folder(test_folder_object):

    folder_id = itemgetter('id')(test_folder_object)

    folder = folder_module.get_folder( folder_id = folder_id )

    assert folder['name'] == test_folder_object['name']

#-----files

def test_create_file(test_file_object):

    name, filetype , folder_id, user_id, file_uri, thumbnail_uri, filesize = itemgetter('name', 'type' , 'folder_id', 'user_id', 'file_uri', 'thumbnail_uri', 'filesize')(test_file_object)

    file_id = file_module.store_file_in_db( name, filetype , folder_id, user_id, file_uri, thumbnail_uri )

    assert file_id == 1



def test_create_file_unexisting_folder_key(test_file_object):

    name, filetype , folder_id, user_id, file_uri, thumbnail_uri, filesize = itemgetter('name', 'type' , 'folder_id', 'user_id', 'file_uri', 'thumbnail_uri', 'filesize')(test_file_object)

    folder_id = 24

    with pytest.raises( ForeignResourceNotFoundException ):
       assert file_module.store_file_in_db( name, filetype , folder_id, user_id, file_uri, thumbnail_uri )


def test_get_file(test_file_object):

    file_id = itemgetter('id')(test_file_object)

    fetched_file = file_module.get_file( id = file_id )

    assert fetched_file['name'] == test_file_object['name']

#---------files and folders inside a parent folder
def test_get_child_folder(test_folder_object, test_folder_object_2):

    child_name, child_parent_id, child_owner_id = itemgetter('name', 'parent_id', 'owner_id')(test_folder_object_2)
    folder_module.store_folder_in_db( child_name, child_parent_id, child_owner_id )

    parent_folder_id = test_folder_object["id"]

    fetched_child_folders = folder_module.list_child_folders( folder_id = parent_folder_id )

    assert fetched_child_folders[0]['name'] == test_folder_object_2['name']


def test_get_files_of_folder(test_folder_object, test_file_object):

    folder_id = test_folder_object["id"]

    fetched_files = folder_module.list_files_of_folder( folder_id = folder_id )

    assert fetched_files[0]['name'] == test_file_object['name']




#---------delete file

def test_soft_delete_file(test_file_object):

    file_id = itemgetter('id')(test_file_object)

    affected_rows = file_module.soft_delete_file( id = file_id )

    assert affected_rows == 1


def test_get_sotf_deleted_file(test_file_object):

    file_id = itemgetter('id')(test_file_object)

    with pytest.raises( ResourceNotFoundException ):
        assert  file_module.get_file( id = file_id )

#----------delete folder



def test_soft_delete_folder(test_folder_object_2):

    folder_id = test_folder_object_2["id"]

    affected_rows = folder_module.soft_delete_folder( folder_id = folder_id )

    assert affected_rows == 1

def test_get_soft_deleted_folder(test_folder_object_2):

    folder_id = itemgetter('id')(test_folder_object_2)

    with pytest.raises( ResourceNotFoundException ):
        fetched_folder = folder_module.get_folder( folder_id = folder_id )


#---------files and folders inside a parent folder afer delete

def test_get_child_folder_after_soft_delete(test_folder_object):

    parent_folder_id = test_folder_object["id"]

    with pytest.raises( ResourceNotFoundException ):
        fetched_child_folders = folder_module.list_child_folders( folder_id = parent_folder_id )
