from flask import Flask, request, send_file
from flask_restx  import Api, Resource,  reqparse, fields, abort
from marshmallow import Schema
import os, json

from ..utils.errors import find_error, ForeignResourceNotFoundException, DBNotConnectedException, ResourceNotFoundException, S3StoreException, ThumbnailNotFoundException
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
    'thumbnail_uri':  fields.String,
    'md5':  fields.String,
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

    @name_space.response(200, 'Ok', file_model)
    @api.doc(responses={ 404: 'File not found',  401: 'Unauthorized', 403: 'Forbiden', 503: 'Service Unavailable' })
    def put(self, id):

        #get and validate data
        try:
            request_data = json.loads(request.form.get('data'))
        except TypeError:
            abort( 400, 'Bad Request. Incorrect Json.' )

        #taken from https://marshmallow.readthedocs.io/en/2.x-line/quickstart.html#partial-loading
        marshmallow_validation = FileSchema().validate(request_data, partial=True)
        validation_error = find_error( marshmallow_validation ) 
        
        if( validation_error != None ):
            abort( 400, 'Bad Request.', details=validation_error )

        try:
            print(request_data)
            updated_file_data = file_manager.update_file_data( id, request_data )
            file_schema = FileSchema()
            return_data = file_schema.dump( updated_file_data )
        except ResourceNotFoundException as e:
            abort( 404, e.message )
        except ( DBNotConnectedException) as e:
            abort( 500, e.message )
        except Exception as e:
            abort( 500, e)
        else:
            return return_data, 200

    @name_space.response(204, 'No Content' ) 
    @api.doc(responses={ 404: 'File not found',  401: 'Unauthorized', 403: 'Forbiden', 503: 'Service Unavailable' })
    def delete(self, id):

        try:
            file_data = file_manager.soft_delete_file( id )
        except ResourceNotFoundException as e:
            abort( 404, e.message )
        except ( DBNotConnectedException) as e:
            abort( 500, e.message )
        except Exception as e:
            abort( 500, e)
        else:
            return {}, 204


@name_space.route('/', strict_slashes = False)
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
        except (ForeignResourceNotFoundException , ResourceNotFoundException) as e:
            abort( 404, e.message )
        except ( DBNotConnectedException, S3StoreException) as e:
            abort( 500, e.message )
        except Exception as e:
            abort( 500, e)
        else:
            file_schema = FileSchema()
            return file_schema.dump( created_file_data ), 201


@name_space.route('/<int:id>/download/<string:filename>')
@api.doc(params={'id': 'File id', 'filename': 'name of file to download'})
class FilesDownload(Resource):

    @name_space.response(200, 'Ok')
    @api.doc(responses={ 404: 'File not found',  401: 'Unauthorized', 403: 'Forbiden', 503: 'Service Unavailable' })
    @api.representation('application/octet-stream')
    def get(self, id, filename):

        try:
            downloaded_file = file_manager.download_file( id )
        except ResourceNotFoundException as e:
            abort( 404, e.message )
        except ( DBNotConnectedException ) as e:
            abort( 500, e.message )
        except Exception as e:
            abort( 500, e)
        else:
            return send_file( filename_or_fp = downloaded_file['body'], mimetype = downloaded_file['mime_type'])


@name_space.route('/<int:id>/thumbnail/<string:filename>')
@api.doc(params={'id': 'File id', 'filename': 'name of file to download as thumbnail'})
class ThumbnailsDownload(Resource):

    @name_space.response(200, 'Ok')
    @api.doc(responses={ 404: 'File not found',  401: 'Unauthorized', 403: 'Forbiden', 503: 'Service Unavailable' })
    @api.representation('application/octet-stream')
    def get(self, id, filename):

        try:
            thumbnail = file_manager.download_thumbnail( id )
        except ResourceNotFoundException as e:
            abort( 404, e.message )
        except ThumbnailNotFoundException as e:
            abort( 404, e.message )
        except ( DBNotConnectedException ) as e:
            abort( 500, e.message )
        except Exception as e:
            abort( 500, e)
        else:
            return send_file( filename_or_fp = thumbnail['image'], mimetype = thumbnail['mime_type'])
            