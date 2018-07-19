import os
import boto3

s3 = boto3.resource('s3')
client = boto3.client('s3',
                       aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], # env vars should be passed with the docker run command
                       aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],) 

def upload_new_models():
    os.system('zip -r models/trained_models.zip models/*')
    client.upload_file('models/trained_models.zip', 'grassroot-nlu','models/')
    print('model upload successful')
    os.system('rm -r models/*')
    print('Running test download...')
    s3.Bucket('grassroot-nlu').download_file('models/', 'models/trained_models.zip')
    print('download success')
    print('unpackaging files...')
    os.system('unzip models/trained_models.zip')
    print('Done.')
    print('Cleaning up..')
    os.remove('models/trained_models.zip')
    print('process complete.')

upload_new_models()