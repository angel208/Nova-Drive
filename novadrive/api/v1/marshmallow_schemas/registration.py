from marshmallow import Schema, fields, post_load, INCLUDE, validates, ValidationError

class AppError(Exception):
    pass

class RegistrationModel(object):
    
    def __init__( self, name ):
        self.name = name

class RegistrationSchema( Schema ):

    #this makes the response have the same order as defined in code
    class Meta:
        ordered = True
        unknown = INCLUDE

    id = fields.Integer() 

    email = fields.String(required=True)
    name = fields.String(required=True)
    last_name = fields.String(required=True)

    password = fields.String(required=True)
    password_confirmation = fields.String(required=True)


    @post_load
    def register_user(self, data):
        return RegistrationModel(**data)


