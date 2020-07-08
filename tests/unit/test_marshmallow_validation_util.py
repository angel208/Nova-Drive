## Something that is untested is broken.
import pytest

from novadrive.api.v1.utils import errors as error_module

##--------- begin of tests

def test_marshmallow_validation_errors(test_marshmallow_validation_errors):

    errors = test_marshmallow_validation_errors

    assert error_module.find_error( errors[0] ) == None
    assert error_module.find_error( errors[1] ) == None
    assert error_module.find_error( errors[2] ) != None

