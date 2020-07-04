## Something that is untested is broken.
import pytest

from novadrive.api.v1.utils import marshmallow_utils

##--------- begin of tests

def test_hello(test_marshmallow_validation_errors):

    errors = test_marshmallow_validation_errors

    assert marshmallow_utils.find_error( errors[0] ) == None
    assert marshmallow_utils.find_error( errors[1] ) == None
    assert marshmallow_utils.find_error( errors[2] ) != None

