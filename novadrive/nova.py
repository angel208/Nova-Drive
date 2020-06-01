#nova drive API v1
from flask import Blueprint
from flask_restx import Api

#imports the namespaces for this version of the api
from novadrive.api.v1.default_controller import name_space as ns_nova

#creates a blueprint
blueprint = Blueprint('nova_api', __name__)

api = Api(blueprint,
    title='Nova Drive API',
    version='1.0',
    description='A description'
)

#adds namespaces (controllers) to this blueprint
#this blueprint will be attached at the app.py in the root folder, with all othe versions of the API.
api.add_namespace(ns_nova)