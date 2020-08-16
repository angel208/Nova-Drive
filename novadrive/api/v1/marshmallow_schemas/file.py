from marshmallow import Schema, fields, post_load, INCLUDE
import urllib

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
    md5 =  fields.String() 
    created =  fields.DateTime( ) 
    updated =  fields.DateTime() 
    deleted =  fields.DateTime() 

    #set file uris in BD
    file_uri = fields.Method("generate_file_url")
    thumbnail_uri =  fields.Method("generate_thumbnail_url")
    
    def generate_file_url(self, obj):
        file_name = obj['name']
        file_id = obj['id']
        file_internal_uri = "/api/v1/files/"+str(file_id)+"/download/"+urllib.parse.quote_plus(file_name)
        return file_internal_uri

    def generate_thumbnail_url(self, obj):
        file_name = obj['name']
        file_id = obj['id']
        thumbnail_internal_uri = "/api/v1/files/"+str(file_id)+"/thumbnail/"+urllib.parse.quote_plus(file_name)
        return  thumbnail_internal_uri

    @post_load
    def create_file(self, data):
        return FileModel(**data)


