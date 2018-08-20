import os
import boto3

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

def upload_new_models():
    """Called by train_models() when a new model comes fresh out of training"""
    os.system('zip -r models/trained_models.zip models/*')
    client.upload_file('models/trained_models.zip', 'grassroot-nlu','models/')
    print('model upload successful')
    os.system('rm -r models/*')

# train_models()
upload_new_models()