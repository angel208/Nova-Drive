from flask import Flask
from flask_restx  import Api, Resource, fields
from ..services import user_manager
import os


flask_app  = Flask(__name__)
api = Api(flask_app)

#creates a namespace for this controller. it allows to separate different controllers from different resources.
name_space = api.namespace('api/v1', version = "1.0", title = "Nova Drive", description = "Simple Cloud based drive made with python, flask and mongodb" )

#default response model
model = name_space.model('Default', {
    'response': fields.String,
})

@name_space.route('/')
class Hello(Resource):
    @name_space.response(200, 'Ok', model)
    @name_space.response(403, 'Forbiden')
    @name_space.response(401, 'Not Authorized')
    def get(self):
        return {
            "status": 'Welcome to Nova Drive!'
        }

    @name_space.response(200, 'Ok', model)
    @name_space.response(403, 'Forbiden')
    @name_space.response(401, 'Not Authorized')
    def post(self):
        return {
            "status": "Posted new data"
        }
