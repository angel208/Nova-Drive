from .session import s3
from botocore.exceptions import ClientError
from ..errors import S3StoreException
import configparser

#get bucket name from config file
config = configparser.ConfigParser()
config.read('config.ini')
bucket_name = config['s3_data']['bucket_name']

def list_buckets():
    return s3.buckets.all()

def store_file( binary_file, file_name, file_type):
    """Upload a file to an S3 bucket

    :param binary_file: File to upload
    :param file_name: S3 object name.
    :return: True if file was uploaded, else False
    """
    try:
        object = s3.Object(bucket_name, file_name)
        object.put(Body = binary_file, ContentType=file_type )
    except ClientError as e:
        print(e)
        return False

    return True

def get_file( file_name ):
    """get a file from an S3 bucket

    :param file_name: S3 object name. 
    :return: File as beam
    """

    try:
        object = s3.Object(bucket_name, file_name)
        stored_file = object.get()
    except ClientError as e:
        print(e)
        return S3StoreException()

    return { 'body' : stored_file['Body'], 'mime_type' : stored_file['ContentType'] }


