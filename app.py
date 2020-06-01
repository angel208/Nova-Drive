from flask import Flask, Blueprint
from flask_restx  import Api, Resource, fields

from novadrive.nova import blueprint as nova_api

#creates flask app
flask_app  = Flask(__name__)

#register de blueprint for the v1 of the API (found in novadrive/nova.py)
flask_app.register_blueprint(nova_api)

#runs app
flask_app.run(debug=True)