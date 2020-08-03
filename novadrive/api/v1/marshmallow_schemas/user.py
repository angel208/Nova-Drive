from marshmallow import Schema, fields, post_load, INCLUDE


class UserModel(object):
    
    def __init__( self, name ):
        self.name = name

class UserSchema( Schema ):

    #this makes the response have the same order as defined in code
    class Meta:
        ordered = True
        unknown = INCLUDE

    id = fields.Integer() 

    name = fields.String()
    last_name = fields.String()
    email = fields.String()
    image = fields.String()
    thumbnail = fields.String()

    root_folder_id =  fields.Integer() 
    remaining_drivespace =  fields.Integer() 

    created =  fields.DateTime( ) 
    updated =  fields.DateTime() 
    deleted =  fields.DateTime() 


    @post_load
    def create_user(self, data):
        return UserModel(**data)


