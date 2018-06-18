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

threshold = 0.6
database = DynamoDB
#database = MongoDB

os.system('aws ecr get-login --region eu-west-1')
os.system('aws s3api get-object --bucket grassroot-nlu --key activation/feersum_setup.sh feersum_setup.sh')
# os.system('source ./feersum_setup.sh')

s3 = boto3.resource('s3')
client = boto3.client('s3',
                       aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], # env vars should be passed with the docker run command
                       aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],) 
# s3 = boto3.resource('s3', default_region='eu-west-1', api_version='2006-03-01')

current_files = os.listdir('./')

word_distance_files = ["vocab.txt", "vectors.txt"]

for file in word_distance_files:
    if file not in current_files:
        s3.Bucket('grassroot-nlu').download_file('word_distance/%s' % file, 
                                                 '%s' % file)

if 'feersum_setup.sh' not in current_files:
    s3.Bucket('grassroot-nlu').download_file('activation/feersum_setup.sh',
                                             'feersum_setup.sh')


files = ['entity_extractor.dat',
         'entity_synonyms.json',
         'intent_classifier.dat',
         'regex_featurizer.json',
         'training_data.json']


for file in files:
    x = s3.Bucket('grassroot-nlu').download_file('models/current_model/%s' % file, 
                                                 './current_model/%s' % file)

print('Retrieving components...')
os.system('sh install_mitie.sh')

def configure():
    print('configuring components...')
    os.environ['PATH_TO_MITIE'] = './current_model/model/MITIE-models/english/total_word_feature_extractor.dat'        

    configuration_1 = {
                       "pipeline": "mitie",
                       "mitie_file": os.environ['PATH_TO_MITIE'],
                       "path" : "./models",
                       "data" : "./training_data.json"
                      }
    configuration_2 = {
                       "language": "en",
                       "pipeline": [
                                    "nlp_mitie",
                                    "tokenizer_mitie",
                                    "ner_mitie",
                                    "ner_synonyms",
                                    "intent_entity_featurizer_regex",
                                    "intent_classifier_mitie"
                                   ],
                       "training_data": "training_data.json",
                       "mitie_feature_extractor_fingerprint": 4070312463,
                       "mitie_file": "./current_model/model/MITIE-models/english/total_word_feature_extractor.dat",
                       "entity_extractor_mitie": "entity_extractor.dat",
                       "entity_synonyms": "entity_synonyms.json",
                       "regex_featurizer": "regex_featurizer.json",
                       "intent_classifier_mitie": "intent_classifier.dat",
                       "trained_at": "20171004-160114",
                       "rasa_nlu_version": "0.9.2"
                       }

    c_file = open('config_mitie.json', 'w')
    c_file.write(json.dumps(configuration_1))
    
    os.system('touch ./current_model/metadata.json')
    m_file = open('./current_model/metadata.json', 'w')
    m_file.write(json.dumps(configuration_2))


configure()
metadata = Metadata.load('./current_model')
interpreter = Interpreter.load(metadata, RasaNLUConfig('config_mitie.json'))
print('components configured')

def generate_training_data():

    if database == MongoDB:
        new_stub = []

        for i in find(database, stub):
            i.pop('_id')
            new_stub.append(i)

        new_stub = new_stub[0]
        ce = new_stub['rasa_nlu_data']['common_examples']

        for i in find(database, common_examples):
            i.pop('_id')
            ce.append(i)

        for i in find(database, runtime_training_data):
            i.pop('_id')
            ce.append(i)

        new_stub = json.dumps(new_stub)
        f = open('training_data.json', 'w')
        f.write(new_stub)
        auto_trainer()

    if database == DynamoDB:
        table = dynamodb.Table('vacuole')
        stub = table.scan()['Items'][0]['payload']
        tab = dynamodb.Table('common_examples')
        ce = tab.scan()['Items'][0]['payload']

        for i in ce:
            stub['rasa_nlu_data']['common_examples'].append(i)

        new_stub = json.dumps(stub, default=default)
        f = open('training_data.json', 'w')
        f.write(new_stub)
        auto_trainer()
        

def auto_trainer():

    print('\n\n')
    
    training_data = load_data('training_data.json')
    trainer = Trainer(RasaNLUConfig('config_mitie.json'))
    trainer.train(training_data)
    model_directory = trainer.persist('./models')+'/'
    files = os.listdir(model_directory)
    start = model_directory.find('model_')

    for file in files: 
        client.upload_file(model_directory+file,'grassroot-nlu','models/'+model_directory[start:]+file)

    print('model upload successful')

    model = {'dir': model_directory}
    os.remove('training_data.json')
    accuracy_check(**model)


def accuracy_check(**model_directory):
    results = []

    for i in examples:
        instance = interpreter.parse(i)
        score = instance['intent']['confidence']
        results.append(score)

    the_sum = sum(results)
    length = len(results)
    avg = the_sum/length
    maxi = max(results)
    print("max: %2.10f\nmin: %2.10f\navg: %2.10f" % (maxi, min(results), avg))

    stored_model_score = './current_model/current_model_score.txt'
    f = open(stored_model_score, 'r')
    value = f.read()

    if value == '':
        f = open(stored_model_score,'w')
        f.write('0.0')
        f.close()

    f = open(stored_model_score, 'r')
    current_model_score = float(f.read())
    f.close()

    if avg > current_model_score:
        f = open(stored_model_score,'w')
        f.write(str(avg))
        
        print('new model score successfuly written')

        if model_directory:

            for file in files:
                client.delete_object(Bucket='grassroot-nlu', Key='models/current_model/'+file)

            for file in files: 
                client.upload_file(model_directory['dir']+file,'grassroot-nlu','models/current_model/'+file)

            print('new model successfully uploaded to s3') 
            src = model_directory['dir']
            dest = './current_model/'

            if 'current_model' in os.listdir():
                shutil.rmtree('./current_model/')

            shutil.copytree(src,dest)
            print('Ready for main script reinitialisation')
            shutil.rmtree('./models')
            os.system('bash restart.sh')
            print('Successfuly reininitialised script with new model.')

        else:
            print('No model specified')

    else:
        if model_directory:
            print("our new model isn't better than the one currently in use. Sustained.")


this_moment = "00:30"

  
schedule.every().day.at(this_moment).do(generate_training_data)


def start_training():
    schedule.run_pending()
    time.sleep(1)

 
# A json override
def default(obj):

    if isinstance(obj, Decimal):
        return int(obj)

    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj))

print('I am configured.')