from ..database.file import get_file

def get_file_data( id ):
    return get_file(id)

def store_file( request_file, request_data ):
    return { 'name' : 'asd '}

