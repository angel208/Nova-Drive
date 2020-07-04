from ..database.file import get_file
from datetime import datetime

def get_file_data( id ):
    return get_file(id)

def store_file( request_file, request_data, user ):

    #data format: {'name' , 'type' , 'folder_id' }
    file_name = request_data['name']
    file_type = request_data['type']
    folder_id = request_data['folder_id']

    print(file_name, file_type, folder_id)

    #get user_id
    user_id = user

    #generate custom file name
    internal_file_name = create_custom_internal_filename( file_name )
    print(internal_file_name)

    #create thumbnail

    #store file into s3

    #store thumbnail into s3

    #store file info in db

    return { 'name' : 'asd '}

def create_custom_internal_filename( file_name ):
    datestamp = datetime.today().strftime('%Y%m%d%H%M%S')
    internal_file_name = datestamp + "_" + file_name
    return internal_file_name
