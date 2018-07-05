print('Loading configurations...')
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.converters import load_data
from rasa_nlu.model import Interpreter, Metadata, Trainer
from databases.poly_database import *
from databases.poly_Mongo import *
from databases.poly_dynamo import *
import schedule
import time
import json
from examples import *
from decimal import Decimal
import os
import shutil
import boto3
print('imports complete.')

threshold = 0.6
database = DynamoDB
#database = MongoDB

os.system('aws ecr get-login --region eu-west-1')
# os.system('aws s3api get-object --bucket grassroot-nlu --key activation/feersum_setup.sh feersum_setup.sh')
# os.system('source ./feersum_setup.sh') 

s3 = boto3.resource('s3')
client = boto3.client('s3',
                       aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], # env vars should be passed with the docker run command
                       aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],) 
"""
current_files = os.listdir('./')

word_distance_files = ["vocab.txt", "vectors.txt"]

for file in word_distance_files:
    if file not in current_files:
        s3.Bucket('grassroot-nlu').download_file('word_distance/%s' % file, 
                                                 '%s' % file)

if 'feersum_setup.sh' not in current_files:
    s3.Bucket('grassroot-nlu').download_file('activation/feersum_setup.sh',
                                             'feersum_setup.sh')
"""

intent_interpreter = 0
vote_interpreter = 0
meeting_interpreter= 0
todo_interpreter = 0
updates_interpreter = 0
group_interpreter = 0


def configure():
    print('configuring components...')
    os.environ['PATH_TO_MITIE'] = './current_model/model/MITIE-models/english/total_word_feature_extractor.dat'        

    try:
        load_interpreters()
    except:
        train_models()
        configure()

def load_interpreters():
    print('configuring interpreters...')
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

    print('components configured')

def train_models():
    os.system('python training_data_maker.py')
        
configure()
print('I am configured.')