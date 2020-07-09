from ..database.file import get_file, store_file_in_db
from ..utils import file_helpers
from ..utils.aws import s3


def get_file_data( id ):
    return get_file(id)

def store_file( request_file, request_data, user ):

    #data format: {'name' , 'folder_id' }
    file_name = request_data['name']
    folder_id = request_data['folder_id']

    #get user_id
    user_id = user

    #generate custom file name
    internal_file_name = file_helpers.create_custom_internal_filename( file_name )
    print(internal_file_name)

    #get file type
    file_type = request_file.content_type
    print(request_file, file_name, file_type, folder_id)

    #get filesize
    file_size = file_helpers.get_file_size(request_file)

    #store file into s3
    s3.store_file( request_file, internal_file_name, file_type )

    #store file info in db
    created_file_id = store_file_in_db(     name = file_name, 
                                            filetype = file_type, 
                                            folder_id = folder_id, 
                                            user_id = user_id, 
                                            file_uri = internal_file_name, 
                                            thumbnail_uri = '' , 
                                            filesize = file_size )

    #store thumbnail into s3

    #create thumbnail
    #if( file_helpers.check_if_image(file_type) ):
        #image_thumbnail = ""

    return get_file( created_file_id )


