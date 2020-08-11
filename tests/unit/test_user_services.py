## Something that is untested is broken.
import pytest
from mock import patch

from novadrive.api.v1.services import user_manager as user_manager

##--------- begin of tests

@patch('novadrive.api.v1.services.user_manager.get_user')
def test_get_user_data( mock_get_user, test_user):
    mock_get_user.return_value = test_user
    user = user_manager.get_user_data( id = 1 )
    assert user['name'] == test_user['name']



