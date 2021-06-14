import configparser
import magic, mimetypes
import os

#get bucket name from config file
config = configparser.ConfigParser()
config.read('config.ini')
storage_path = config['file_storage']['storage_path']


def store_file( binary_file, file_name, file_type ):
    """Upload a file to local file storage

    :param binary_file: File to upload
    :param file_name: file name.
    :return: True if file was uploaded, else False
    """
    try:
        file_extension = mimetypes.guess_extension(file_type)
        binary_file.save(os.path.join(storage_path, file_name + file_extension ))
        return True
    except Exception as e:
        print(e)
        return False
    

def store_thumbnail( image_file, file_name, file_type ):
    """Upload a file to local file storage (in ths thumbnail subfolder)

    :param image_file: PIL image to upload
    :param file_name: file name.
    :return: True if file was uploaded, else False
    """
    try:
        file_extension = mimetypes.guess_extension(file_type)
        image_file.save(os.path.join(storage_path, "thumbnails/" ,file_name + file_extension) )
        return True
    except Exception as e:
        print(e)
        return False

def get_file( file_name ):
    """get a file path from local file storage

    :param file_name: file storage file name. 
    :return: File as beam
    """

    #data = storage_path + file_name
    path = storage_path + file_name


    mime = magic.Magic(mime=True)
    mimetype = mime.from_file(path)

    
    return { 'body' : path, 'mime_type' : mimetype }


