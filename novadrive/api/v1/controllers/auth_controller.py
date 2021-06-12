from flask import Flask, request,redirect
from flask_restx  import Api, Resource,  reqparse, fields, abort 
from marshmallow import Schema
import os, json

from ..utils.errors import find_error, UserAlreadyExistsException, DBNotConnectedException
from ..services import user_manager, folder_manager ##
from ..marshmallow_schemas.registration import RegistrationSchema
from ..marshmallow_schemas.user import UserSchema


flask_app  = Flask(__name__)
api = Api(flask_app )

#creates a namespace for this controller. it allows to separate different controllers from different resources.
name_space = api.namespace('api/v1/account', version = "1.0", title = "Nova Drive", description = "Auth Management" )

#documentation models ####################
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



@name_space.route('/register')
class UserRegistrationResource(Resource):


    @name_space.response(400, 'Bad Request')
    @api.doc(responses={ 503: 'Service Unavailable' }) ###########
    def post(self):

        #get and validate data
        try:
            request_data = request.json 
        except TypeError:
            abort( 400, 'Bad Request. Incorrect JSON.' )

        if( request_data is None):
            abort( 400, 'Bad Request. Incorrect or unexistent JSON.' )

        marshmallow_validation = RegistrationSchema().validate(request_data)
        validation_error = find_error( marshmallow_validation ) 
        
        if( validation_error != None ):
            abort( 400, 'Bad Request.', details=validation_error )

        print(request_data)   
               
        #create user
        try:
            created_user_data = user_manager.create_user( request_data )
        except UserAlreadyExistsException as e:
            abort( 400, e.message )
        except ( DBNotConnectedException) as e:
            abort( 500, e.message )
        except Exception as e:
            abort( 500, e)
        else:
            folder_schema =  UserSchema()
            return folder_schema.dump( created_user_data ), 201

   