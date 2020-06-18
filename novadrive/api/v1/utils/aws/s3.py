from session import s3
from botocore.exceptions import ClientError
import configparser

#get bucket name from config file
config = configparser.ConfigParser()
config.read('config.ini')
bucket_name = config['s3_data']['bucket_name']

def list_buckets():
    return s3.buckets.all()

def store_file( binary_file, file_name):
    """Upload a file to an S3 bucket

    :param binary_file: File to upload
    :param file_name: S3 object name.
    :return: True if file was uploaded, else False
    """
    try:
        object = s3.Object(bucket_name, file_name)
        object.put(Body = binary_file)
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
        return None

    return stored_file['Body'].read()


