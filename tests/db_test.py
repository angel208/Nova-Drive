## Something that is untested is broken.
import pytest
from novadrive.api.v1.database import user as user_module

##--------- begin of tests

def test_get_user(test_users):

    user = user_module.get_user( id = 1 )
    assert user['name'] == test_users[0]['name']

