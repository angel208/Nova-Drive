from ..database.file import get_file_data as get_file_data_from_db, store_file_in_db, soft_delete_file as delete_file_from_db
from ..utils import file_helpers
from ..utils.aws import s3
from ..utils.file_storage import file_storage


def get_file_data( file_id ):
    return get_file_data_from_db(file_id)

def soft_delete_file( file_id ):
    return delete_file_from_db(file_id)

def store_file( request_file, request_data, user ):

    #data format: {'name' , 'folder_id' }
    user_file_name = request_data['name']
    folder_id = request_data['folder_id']

    #get user_id
    user_id = user

    #generate custom file name
    internal_user_file_name = file_helpers.create_custom_internal_filename( user_file_name )
    print(internal_user_file_name)

    #get file type
    file_type = request_file.content_type
    print(request_file, user_file_name, file_type, folder_id)

    #get filesize
    file_size = file_helpers.get_file_size(request_file)

    #calculate HASH of the file
    file_md5 = file_helpers.calculate_md5( request_file )

    #store file into s3
    file_storage.store_file( request_file, internal_user_file_name , file_type )

    #store file info in db
    created_file_id = store_file_in_db(     name = user_file_name, 
                                            filetype = file_type, 
                                            folder_id = folder_id, 
                                            user_id = user_id, 
                                            internal_filename = internal_user_file_name,
                                            filesize = file_size,
                                            md5 = file_md5
                                            
                                        )

    #create thumbnail
    #if( file_helpers.check_if_image(file_type) ):
        #image_thumbnail = ""

     #store thumbnail into s3
    
    return get_file_data_from_db( created_file_id )

def download_file( file_id ):

    file_data = get_file_data_from_db(file_id)

    internal_filename = file_data["internal_filename"]
    file_name = file_data["name"]

    downloaded_file = file_storage.get_file(internal_filename)
    downloaded_file['file_name'] = file_name

    return downloaded_file


def generate_thumbnail( file_id ):

    file_data = get_file_data_from_db(file_id)

    internal_filename = file_data["internal_filename"]
    file_name = file_data["name"]

    downloaded_file = file_storage.get_file(internal_filename)
    downloaded_file['file_name'] = file_name

    return downloaded_file


