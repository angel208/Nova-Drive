#nova drive API v1
from flask import Blueprint
from flask_restx import Api

#imports the namespaces for this version of the api
from novadrive.api.v1.controllers.default_controller import name_space as nova_ns
from novadrive.api.v1.controllers.file_controller import name_space as file_ns
from novadrive.api.v1.controllers.folder_controller import name_space as folder_ns
from novadrive.api.v1.controllers.user_controller import name_space as user_ns

#creates a blueprint
blueprint = Blueprint('nova_api', __name__)

api = Api(blueprint,
    title='Nova Drive API',
    version='1.0',
    description='A description'
)

#adds namespaces (controllers) to this blueprint
#this blueprint will be attached at the app.py in the root folder, with all othe versions of the API.
api.add_namespace(nova_ns)
api.add_namespace(file_ns)
api.add_namespace(folder_ns)
api.add_namespace(user_ns)