from flask import Flask, request 
from flask_restx  import Api, Resource, fields
from ..services import file_manager
import os, json 


flask_app  = Flask(__name__)
api = Api(flask_app)

#creates a namespace for this controller. it allows to separate different controllers from different resources.
name_space = api.namespace('api/v1/files', version = "1.0", title = "Nova Drive", description = "File Management" )

#default response model
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
    'type': fields.String(description='.jpg, .png, .doc, .pdf, etc.'),
    'folder_id':  fields.Integer,
})

@name_space.route('/<int:id>')
@api.doc(params={'id': 'File id'})
class FilesResource(Resource):

    @name_space.response(200, 'Ok', file_model)
    @api.doc(responses={ 404: 'File not found',  401: 'Unauthorized', 403: 'Forbiden', 503: 'Service Unavailable' })
    @api.marshal_with(file_model, envelope='resource')

    def get(self, id):
        file_data = file_manager.get_file_data( id )
        return file_data

    

@name_space.route('/')
class FilesController(Resource):

    @name_space.response(400, 'Bad Request or filsize too big for remaining storage')
    @api.doc(responses={ 404: 'File not found',  401: 'Unauthorized', 403: 'Forbiden', 503: 'Service Unavailable' })
    @name_space.expect(post_file_model)
    @api.marshal_with(file_model,  code=201, envelope='resource')
    def post(self):

        request_data = json.loads(request.form.get('data'))
        request_file = request.files['file']

        created_file = file_manager.store_file( request_file, request_data )
       
        return created_file, 201