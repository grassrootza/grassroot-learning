import os
import boto3
"""A test script that checks whether the model download and upload routine 
works"""

s3 = boto3.resource('s3')
client = boto3.client('s3',
                       aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], # env vars should be passed with the docker run command
                       aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],)

def train_models():
    """Activates training_data_maker.py and uploads generated model to s3 if
    internet connection exists."""
    os.system('python3 training_data_maker.py')
    try:
        upload_new_models()
    except Exception as e:
        pass

def try_download_models():
    """Attempts to download models from s3 and calls train_models if unsuccessful."""
    try:
        s3.Bucket('grassroot-nlu').download_file('models/', 'models/trained_models.zip')
        print('download success')
        print('unpackaging files...')
        os.system('unzip -o models/trained_models.zip')
        print('Done.')
        print('Cleaning up..')
        os.remove('models/trained_models.zip')
        print('model download and cleanup complete.')
        os.system('python3 generate_mities.py')
    except Exception as e:
        print(str(e))
        train_models()

def upload_new_models():
    """Called by train_models() when a new model comes fresh out of training"""
    os.system('zip -r models/trained_models.zip models/*')
    client.upload_file('models/trained_models.zip', 'grassroot-nlu','models/')
    print('model upload successful')
    os.system('rm -r models/*')

# train_models()
try_download_models()
upload_new_models()
