from marshmallow import Schema, fields, post_load, INCLUDE
from .file import FileSchema

class FolderModel(object):
    
    def __init__( self, name, parent_id, owner_id ):
        self.name = name
        self.parent_id = parent_id
        self.owner_id = owner_id  

class FolderSchema( Schema ):

    #this makes the response have the same order as defined in code
    class Meta:
        ordered = True
        unknown = INCLUDE

    id = fields.Integer() 

    name = fields.String(required=True)
    parent_id = fields.Integer(required=True)

    owner_id =  fields.Integer() 
    created =  fields.DateTime( ) 
    updated =  fields.DateTime() 
    deleted =  fields.DateTime() 

     
    files   = fields.List( fields.Nested(FileSchema) )
    folders = fields.List( fields.Nested( lambda: FolderSchema() ) )


    @post_load
    def create_folder(self, data):
        return FolderModel(**data)


