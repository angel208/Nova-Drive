from flask import Flask, request,redirect
from flask_restx  import Api, Resource,  reqparse, fields, abort 
from marshmallow import Schema
import os, json

from ..utils.errors import find_error, ForeignResourceNotFoundException, DBNotConnectedException, ResourceNotFoundException
from ..services import user_manager, folder_manager
from ..marshmallow_schemas.folder import FolderSchema
from ..marshmallow_schemas.user import UserSchema


flask_app  = Flask(__name__)
api = Api(flask_app )

#creates a namespace for this controller. it allows to separate different controllers from different resources.
name_space = api.namespace('api/v1/users', version = "1.0", title = "Nova Drive", description = "User Management" )

#documentation models
user_model = name_space.model('User', {
    'id': fields.Integer,
    'name': fields.String,
    'last_name': fields.String,
    'email':  fields.String,
    'image':  fields.String,
    'thumbnail': fields.String,
    'remaining_drivespace': fields.Integer,
    'root_folder_id': fields.Integer,
    'created':  fields.DateTime(dt_format='rfc822'),
    'updated':  fields.DateTime(dt_format='rfc822'),
    'deleted':  fields.DateTime(dt_format='rfc822'),
})

folder_model = name_space.model('Folder', {
    'id': fields.Integer,
    'name': fields.String,
    'parent_id':  fields.Integer,
    'owner_id':  fields.Integer,
    'created':  fields.DateTime(dt_format='rfc822'),
    'updated':  fields.DateTime(dt_format='rfc822'),
    'deleted':  fields.DateTime(dt_format='rfc822'),
})



@name_space.route('/<int:id>')
@api.doc(params={'id': 'User id'})
class FoldersResource(Resource):

    @name_space.response(200, 'Ok', user_model)
    @api.doc(responses={ 404: 'User not found',  401: 'Unauthorized', 403: 'Forbiden', 503: 'Service Unavailable' })
    def get(self, id):

        try:
            user_data = user_manager.get_user_data( id )
            user_schema = UserSchema()
            return_data = user_schema.dump( user_data )
        except ResourceNotFoundException as e:
            abort( 404, e.message )
        except ( DBNotConnectedException) as e:
            abort( 500, e.message )
        except Exception as e:
            abort( 500, e)
        else:
            return return_data, 200

   
@name_space.route('/<int:id>/drive')
@api.doc(params={'id': 'User Drive'})
class FoldersResource(Resource):

    @name_space.response(200, 'Ok', folder_model)
    @api.doc(responses={ 404: 'User not found',  401: 'Unauthorized', 403: 'Forbiden', 503: 'Service Unavailable' })
    def get(self, id):

        try:

            folder = folder_manager.get_root_folder_content( user_id = id )
            folder_schema = FolderSchema()
            return_data = folder_schema.dump( folder )

        except ResourceNotFoundException as e:
            abort( 404, e.message )
        except ( DBNotConnectedException) as e:
            abort( 500, e.message )
        except Exception as e:
            abort( 500, e)
        else:
            return return_data, 200