from ..database.folder import get_folder, store_folder_in_db, soft_delete_folder, list_child_folders, list_files_of_folder
from ..database.user import get_user
from ..utils import file_helpers
from ..utils.aws import s3


def get_folder_data( id ):
    return get_folder(id)


def get_folder_content( id ):
    folder = get_folder(id)
    childs = list_child_folders(id)
    files = list_files_of_folder(id)

    folder['files']   = files
    folder['folders'] = childs

    return folder


def get_root_folder_content( user_id ):

    user = get_user( user_id )
    root_folder_id = user['root_folder_id']

    folder = get_folder(root_folder_id)
    childs = list_child_folders(root_folder_id)
    files = list_files_of_folder(root_folder_id)

    folder['files']   = files
    folder['folders'] = childs

    return folder

def delete_folder( id ):
    return soft_delete_folder(id)

def create_folder( request_data, user ):

    #data format: {'name' , 'parent_id' }
    folder_name = request_data['name']
    parent_id = request_data['parent_id']

    #get user_id
    user_id = user

    #store folder info in db
    created_folder_id = store_folder_in_db(   name = folder_name, 
                                            parent_id = parent_id, 
                                            owner_id = user_id )

    return get_folder( created_folder_id )


