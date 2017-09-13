from pymongo import MongoClient
import pprint
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.converters import load_data
from rasa_nlu.model import Interpreter, Metadata, Trainer
from pymongo import MongoClient
import schedule
import time
import json
from examples import *


client = MongoClient()
db = client.database
collection = db.collection
entries = db.entries
stub = db.stub
common_examples = db.common_examples

metadata = Metadata.load('/home/frtnx/models/model_20170902-181024')
interpreter = Interpreter.load(metadata, RasaNLUConfig('/home/frtnx/anaconda3/lib/python3.6/site-packages/rasa_nlu/config_mitie.json'))

def generate_training_data():
    new_stub = []
    for i in stub.find():
        i.pop('_id')
        new_stub.append(i)
    new_stub = new_stub[0]
    ce = new_stub['rasa_nlu_data']['common_examples']
    for i in common_examples.find():
        i.pop('_id')
        ce.append(i)
    new_stub = json.dumps(new_stub)
    f = open('/home/frtnx/grassroot-nlu/training_data.json', 'w')
    f.write(new_stub)
    auto_trainer()


def auto_trainer():
    accuracy_check()
    print('\n\n')
    training_data = load_data('/home/frtnx/grassroot-nlu/training_data.json')
    trainer = Trainer(RasaNLUConfig('/home/frtnx/grassroot-nlu/config_mitie.json'))
    trainer.train(training_data)
    model_directory = trainer.persist('/home/frtnx/models')
    global metadata
    global interpreter
    metadata = Metadata.load(model_directory)
    interpreter = Interpreter.load(metadata, RasaNLUConfig('/home/frtnx/grassroot-nlu/config_mitie.json'))
    accuracy_check()

def accuracy_check():
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
