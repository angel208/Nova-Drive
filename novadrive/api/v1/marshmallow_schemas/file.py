from marshmallow import Schema, fields, post_load, INCLUDE

class FileModel(object):
    def __init__( self, name, folder_id, user_id, file_uri, thumbnail_uri = ''   , filesize = 0 ):
        self.name = name
        self.folder_id = folder_id 

class FileSchema( Schema ):

    #this makes the response have the same order as defined in code
    class Meta:
        ordered = True
        unknown = INCLUDE

    id = fields.Integer() 

    name = fields.String(required=True)
    folder_id = fields.Integer(required=True)

    type = fields.String()
    filesize =  fields.Integer() 
    user_id =  fields.Integer() 
    file_uri =  fields.String() 
    thumbnail_uri =  fields.String() 
    created =  fields.DateTime( ) 
    updated =  fields.DateTime() 
    deleted =  fields.DateTime() 
    

    @post_load
    def create_file(self, data):
        return FileModel(**data)


