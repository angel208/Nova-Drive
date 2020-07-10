from flask import Flask, request 
from flask_restx  import Api, Resource,  reqparse, fields, abort
from marshmallow import Schema
import os, json

from ..utils.errors import find_error, ForeignResourceNotFoundException, DBNotConnectedException, ResourceNotFoundException
from ..services import file_manager
from ..utils import aux_functions, file_helpers
from ..marshmallow_schemas.file import FileSchema


flask_app  = Flask(__name__)
api = Api(flask_app )

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
    'folder_id':  fields.Integer,
})



@name_space.route('/<int:id>')
@api.doc(params={'id': 'File id'})
class FilesResource(Resource):

    @name_space.response(200, 'Ok', file_model)
    @api.doc(responses={ 404: 'File not found',  401: 'Unauthorized', 403: 'Forbiden', 503: 'Service Unavailable' })
    def get(self, id):

        try:
            file_data = file_manager.get_file_data( id )
            file_schema = FileSchema()
            return_data = file_schema.dump( file_data )
        except ResourceNotFoundException as e:
            abort( 404, e.message )
        except ( DBNotConnectedException) as e:
            abort( 500, e.message )
        except Exception as e:
            abort( 500, e)
        else:
            return return_data, 200


@name_space.route('/')
class FilesController(Resource):

    @name_space.response(400, 'Bad Request or filesize too big for remaining storage')
    @api.doc(responses={ 404: 'Folder or user not found',  401: 'Unauthorized', 403: 'Forbiden', 503: 'Service Unavailable' })
    def post(self):

        #get and validate data
        try:
            request_data = json.loads(request.form.get('data'))
        except TypeError:
            abort( 400, 'Bad Request. Incorrect Json.' )

        marshmallow_validation = FileSchema().validate(request_data)
        validation_error = find_error( marshmallow_validation ) 
        
        if( validation_error != None ):
            abort( 400, 'Bad Request.', details=validation_error )
        
        #get and validate file
        request_file = None
        
        if 'file' in request.files:
            request_file = request.files['file']
        else:
            abort( 400, 'Bad Request: missing file in request body.' )

        file_size = file_helpers.get_file_size(request_file)
        app_config_max_size = aux_functions.get_app_config('max_file_size')
        
        if( file_size > int(app_config_max_size) ):
            abort( 400, 'Bad Request: file too big. Current max size of upladed files is ' + app_config_max_size + " Bytes." )
        
        #store file
        try:
            created_file_data = file_manager.store_file( request_file, request_data, '1' )
        except ForeignResourceNotFoundException as e:
            abort( 404, e.message )
        except ( DBNotConnectedException, S3StoreException) as e:
            abort( 500, e.message )
        except Exception as e:
            abort( 500, e)
        else:
            file_schema = FileSchema()
            return file_schema.dump( created_file_data ), 201


