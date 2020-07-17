from flask import Flask, request 
from flask_restx  import Api, Resource,  reqparse, fields, abort
from marshmallow import Schema
import os, json

from ..utils.errors import find_error, ForeignResourceNotFoundException, DBNotConnectedException, ResourceNotFoundException
from ..services import folder_manager
from ..marshmallow_schemas.folder import FolderSchema


flask_app  = Flask(__name__)
api = Api(flask_app )

#creates a namespace for this controller. it allows to separate different controllers from different resources.
name_space = api.namespace('api/v1/folders', version = "1.0", title = "Nova Drive", description = "Folder Management" )

#models
folder_model = name_space.model('Folder', {
    'id': fields.Integer,
    'name': fields.String,
    'parent_id':  fields.Integer,
    'owner_id':  fields.Integer,
    'created':  fields.DateTime(dt_format='rfc822'),
    'updated':  fields.DateTime(dt_format='rfc822'),
    'deleted':  fields.DateTime(dt_format='rfc822'),
})

post_folder_model = name_space.model('Post Folder', {
    'name': fields.String,
    'parent_id':  fields.Integer,
})


@name_space.route('/<int:id>')
@api.doc(params={'id': 'Folder id'})
class FoldersResource(Resource):

    @name_space.response(200, 'Ok', folder_model)
    @api.doc(responses={ 404: 'Folder not found',  401: 'Unauthorized', 403: 'Forbiden', 503: 'Service Unavailable' })
    def get(self, id):

        try:
            folder_data = folder_manager.get_folder_data( id )
            folder_schema = FolderSchema()
            return_data = folder_schema.dump( folder_data )
        except ResourceNotFoundException as e:
            abort( 404, e.message )
        except ( DBNotConnectedException) as e:
            abort( 500, e.message )
        except Exception as e:
            abort( 500, e)
        else:
            return return_data, 200

    @name_space.response(204, 'No Content' ) 
    @api.doc(responses={ 404: 'Folder not found',  401: 'Unauthorized', 403: 'Forbiden', 503: 'Service Unavailable' })
    def delete(self, id):

        try:
            folder_data = folder_manager.delete_folder( id )
        except ResourceNotFoundException as e:
            abort( 404, e.message )
        except ( DBNotConnectedException) as e:
            abort( 500, e.message )
        except Exception as e:
            abort( 500, e)
        else:
            return {}, 204


@name_space.route('/')
class FoldersController(Resource):

    @name_space.response(400, 'Bad Request')
    @api.doc(responses={ 404: 'Folder not found',  401: 'Unauthorized', 403: 'Forbiden', 503: 'Service Unavailable' })
    def post(self):

        #get and validate data
        try:
            request_data = request.json 
        except TypeError:
            abort( 400, 'Bad Request. Incorrect JSON.' )

        if( request_data is None):
            abort( 400, 'Bad Request. Incorrect or unexistent JSON.' )

        marshmallow_validation = FolderSchema().validate(request_data)
        validation_error = find_error( marshmallow_validation ) 
        
        if( validation_error != None ):
            abort( 400, 'Bad Request.', details=validation_error )
        
               
        #create folder
        try:
            created_folder_data = folder_manager.create_folder( request_data, '1' )
        except ForeignResourceNotFoundException as e:
            abort( 404, e.message )
        except ( DBNotConnectedException) as e:
            abort( 500, e.message )
        except Exception as e:
            abort( 500, e)
        else:
            folder_schema =  FolderSchema()
            return folder_schema.dump( created_folder_data ), 201
