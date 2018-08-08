from logger import rootLogger
rootLogger.info('Loading configurations...')
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.converters import load_data
from rasa_nlu.model import Interpreter, Metadata, Trainer
from databases.poly_database import *
from databases.poly_Mongo import *
from databases.poly_dynamo import *
import schedule
import threading
import time
import json
from decimal import Decimal
import os
import shutil
import boto3
rootLogger.info('imports complete.')

threshold = 0.6
database = DynamoDB
# database = MongoDB

# os.system('aws ecr get-login --region eu-west-1')
# os.system('aws s3api get-object --bucket grassroot-nlu --key activation/feersum_setup.sh feersum_setup.sh')
# os.system('source ./feersum_setup.sh') 

s3 = boto3.resource('s3')
client = boto3.client('s3',
                       aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], # env vars should be passed with the docker run command
                       aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],) 

# current_files = os.listdir('./')

# word_distance_files = ["vocab.txt", "vectors.txt"]

# for file in word_distance_files:
#     if file not in current_files:
#         s3.Bucket('grassroot-nlu').download_file('word_distance/%s' % file, 
#                                                 '%s' % file)

# if 'feersum_setup.sh' not in current_files:
#     s3.Bucket('grassroot-nlu').download_file('activation/feersum_setup.sh',
#                                              'feersum_setup.sh')

intent_interpreter = 0
vote_interpreter = 0
meeting_interpreter= 0
todo_interpreter = 0
updates_interpreter = 0
group_interpreter = 0


def configure():
    """Main configuration automator. Responsible for call other configuration functions.
    Tries configuring nlu engine in current state, downloads models from s3 if absent,
    trains new models locally on host if s3 models cannot be obtained."""
    rootLogger.info('configuring components...')
    try:
        load_interpreters()
    except Exception as e:
        print(str(e))
        print("Dont worry, I'll take care of this\ndeploying counter-measures...")
        threading.Thread(target=try_download_models).start()
        print('putting baby to sleep...')
        time.sleep(30)
        print('baby is up and screaming.')
        configure()


def load_interpreters():
    """Loads interpreters and their respective metadatas"""
    rootLogger.debug('configuring interpreters...')
    global intent_interpreter
    global vote_interpreter
    global meeting_interpreter
    global todo_interpreter
    global updates_interpreter
    global group_interpreter
    intent_metadata = Metadata.load('./models/intent/default/%s' % os.listdir('./models/intent/default/')[0])
    meeting_metadata = Metadata.load('./models/meeting/default/%s' % os.listdir('./models/meeting/default/')[0])
    vote_metadata = Metadata.load('./models/vote/default/%s' % os.listdir('./models/vote/default/')[0])
    todo_metadata = Metadata.load('./models/todo/default/%s' % os.listdir('./models/todo/default/')[0])
    updates_metadata = Metadata.load('./models/updates/default/%s' % os.listdir('./models/updates/default/')[0])
    group_metadata = Metadata.load('./models/group/default/%s' % os.listdir('./models/group/default/')[0])

    intent_interpreter = Interpreter.load(intent_metadata, RasaNLUConfig('intent_config_mitie.json'))
    vote_interpreter = Interpreter.load(vote_metadata, RasaNLUConfig('vote_config_mitie.json'))
    meeting_interpreter = Interpreter.load(meeting_metadata, RasaNLUConfig('meeting_config_mitie.json'))
    todo_interpreter = Interpreter.load(todo_metadata, RasaNLUConfig('todo_config_mitie.json'))
    updates_interpreter = Interpreter.load(updates_metadata, RasaNLUConfig('updates_config_mitie.json'))
    group_interpreter = Interpreter.load(group_metadata, RasaNLUConfig('group_config_mitie.json'))
    rootLogger.debug('components configured')

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

        
configure()
rootLogger.debug('I am configured.')