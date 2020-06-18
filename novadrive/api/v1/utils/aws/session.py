import boto3
from os import environ

session = boto3.Session(
    aws_access_key_id= environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key= environ.get('AWS_SECRET_ACCESS_KEY'),
)

s3 = session.resource('s3')
