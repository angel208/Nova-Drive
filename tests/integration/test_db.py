## Something that is untested is broken.
import pytest
from novadrive.api.v1.database import user as user_module
from novadrive.api.v1.database import folder as folder_module

from operator import itemgetter
from mysql.connector import errors as mysqlErrors

##--------- begin of tests

def test_get_user(test_user):

    user = user_module.get_user( id = 1 )
    assert user['name'] == test_user['name']

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

