from flask import Flask, Blueprint, g
from flask_restx  import Api, Resource, fields
import configparser, os

from novadrive.nova import blueprint as nova_api

def create_app( environment = 'DEV' ):
    #creates flask app
    flask_app  = Flask(__name__)
    #disable the default 404 error, so we can return our own message
    flask_app.config['ERROR_404_HELP'] = False

    os.environ['NOVA_ENV'] = environment

    with flask_app.app_context():
        #register de blueprint for the v1 of the API (found in novadrive/nova.py)
        flask_app.register_blueprint(nova_api)
        return flask_app

#runs app
if __name__ == "__main__":
    #set testing to true
    app = create_app()
    app.run(debug=True)