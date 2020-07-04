from flask import Flask, request 
from flask_restx  import Api, Resource,  reqparse, fields
from marshmallow import Schema
from ..services import file_manager
from ..utils import marshmallow_utils
import os, json 

from ..marshmallow_schemas.file import FileSchema

flask_app  = Flask(__name__)
api = Api(flask_app)

#creates a namespace for this controller. it allows to separate different controllers from different resources.
name_space = api.namespace('api/v1/files', version = "1.0", title = "Nova Drive", description = "File Management" )

#models
file_model = name_space.model('File', {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.String(description='.jpg, .png, .doc, .pdf, etc.'),
    'filesize':  fields.Integer,
    'folder_id':  fields.Integer,
    'user_id':  fields.Integer,
    'file_uri':  fields.String,
    'thumbnail_uri':  fields.String,
    'created':  fields.DateTime(dt_format='rfc822'),
    'updated':  fields.DateTime(dt_format='rfc822'),
    'deleted':  fields.DateTime(dt_format='rfc822'),
})

post_file_model = name_space.model('Post File', {
    'name': fields.String,
    'type': fields.String(description='.jpg, .png, .doc, .pdf, etc.', required=True),
    'folder_id':  fields.Integer,
})



@name_space.route('/<int:id>')
@api.doc(params={'id': 'File id'})
class FilesResource(Resource):

    @name_space.response(200, 'Ok', file_model)
    @api.doc(responses={ 404: 'File not found',  401: 'Unauthorized', 403: 'Forbiden', 503: 'Service Unavailable' })
    def get(self, id):

        file_data = file_manager.get_file_data( id )

        file_schema = FileSchema()
                
        return file_schema.dump( file_data )

    

@name_space.route('/')
class FilesController(Resource):

    @name_space.response(400, 'Bad Request or filesize too big for remaining storage')
    @api.doc(responses={ 404: 'Folder or user not found',  401: 'Unauthorized', 403: 'Forbiden', 503: 'Service Unavailable' })
    def post(self):

        #get data and file
        request_data = json.loads(request.form.get('data'))
        request_file = request.files['file']

        #validate data
        marshmallow_validation = FileSchema().validate(request_data)
        validation_error = marshmallow_utils.find_error( marshmallow_validation ) 

        if( validation_error != None ):
            return validation_error, 400

        #validate file and filesize

        
        #create file
        created_file_data = file_manager.store_file( request_file, request_data, '1' )

        return created_file_data, 201


