import configparser
import magic, mimetypes
import os

#get bucket name from config file
config = configparser.ConfigParser()
config.read('config.ini')
storage_path = config['file_storage']['storage_path']
configured_thumbnail_mime_type = config['app_config']['thumbnail_mime_type']


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
    

def store_thumbnail( image_file, file_name ):
    """Upload a file to local file storage (in ths thumbnail subfolder)

    :param image_file: PIL image to upload
    :param file_name: file name.
    :return: thumbnails uri, else unassigned
    """
    try:
        file_extension = mimetypes.guess_extension(configured_thumbnail_mime_type)
        thumbnail_uri =  os.path.join("thumbnails/" , file_name + file_extension)

        image_file.save(os.path.join(storage_path, thumbnail_uri))
        return thumbnail_uri
    except Exception as e:
        print(e)
        return "unassigned"

def get_file( file_name, file_type ):
    """get a file path from local file storage

    :param file_name: file storage file name. 
    :return: File as beam
    """

    file_extension = mimetypes.guess_extension(file_type)
    path = os.path.join(storage_path, file_name + file_extension)


    mime = magic.Magic(mime=True)
    mimetype = mime.from_file(path)

    
    return { 'body' : path, 'mime_type' : mimetype }


def retrieve_thumbnail( thumbnail_uri ):
    """get a file path from local thumbnail storage

    :param thumbnail_name: file storage file name. 
    :return: File as beam
    """
    path = os.path.join(storage_path, thumbnail_uri)

    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(path)

    return { 'image' : path, 'mime_type' : mime_type }


