## Something that is untested is broken.
import pytest
from operator import itemgetter
from mysql.connector import errors as mysqlErrors

from novadrive.api.v1.database import user as user_module
from novadrive.api.v1.database import folder as folder_module
from novadrive.api.v1.database import file as file_module

##--------- users

def test_get_user(test_user):

    user = user_module.get_user( id = 1 )
    assert user['name'] == test_user['name']

#----------folders

def test_create_folder(test_folder_object):

    name, parent_id, owner_id = itemgetter('name', 'parent_id', 'owner_id')(test_folder_object)

    folder_id = folder_module.create_folder( name, parent_id, owner_id )

    assert folder_id == 1


def test_create_folder_unexisting_parent_key(test_folder_object):

    name, parent_id, owner_id = itemgetter('name', 'parent_id', 'owner_id')(test_folder_object)
    parent_id = 24

    with pytest.raises( mysqlErrors.IntegrityError ):
       assert folder_module.create_folder( name, parent_id, owner_id )

def test_get_folder(test_folder_object):

    folder_id = itemgetter('id')(test_folder_object)

    folder = folder_module.get_folder( id = folder_id )

    assert folder['name'] == test_folder_object['name']

#-----files

def test_create_file(test_file_object):

    name, filetype , folder_id, user_id, file_uri, thumbnail_uri, filesize = itemgetter('name', 'type' , 'folder_id', 'user_id', 'file_uri', 'thumbnail_uri', 'filesize')(test_file_object)

    file_id = file_module.create_file( name, filetype , folder_id, user_id, file_uri, thumbnail_uri )

    assert file_id == 1



def test_create_file_unexisting_folder_key(test_file_object):

    name, filetype , folder_id, user_id, file_uri, thumbnail_uri, filesize = itemgetter('name', 'type' , 'folder_id', 'user_id', 'file_uri', 'thumbnail_uri', 'filesize')(test_file_object)

    folder_id = 24

    with pytest.raises( mysqlErrors.IntegrityError ):
       assert file_module.create_file( name, filetype , folder_id, user_id, file_uri, thumbnail_uri )


def test_get_file(test_file_object):

    file_id = itemgetter('id')(test_file_object)

    created_file = file_module.get_file( id = file_id )

    assert created_file['name'] == test_file_object['name']