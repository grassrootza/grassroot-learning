from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.converters import load_data
from rasa_nlu.model import Interpreter, Metadata, Trainer
from poly_database import *
from poly_Mongo import *
import schedule
import time
import json
from examples import *
import os
import shutil


threshold = 0.6
new_model_checker = []
# The below function returns the latest model in a directory of many models.

"""def find_latest_model(model_dir):
    instances = os.listdir(model_dir)
    leng = len(instances)
    latest = 0
    pro = ''
    for i in range(0, leng):
        raw = instances[i][6:21]
        clean = raw.replace('-','.')
        if float(clean) > latest:
            latest = float(clean)
            pro = instances[i]
    return model_dir+pro
"""
database = MongoDB

metadata = Metadata.load('/home/frtnx/current_model')
interpreter = Interpreter.load(metadata, RasaNLUConfig('/home/frtnx/grassroot-nlu/config_mitie.json'))

def generate_training_data():
    new_stub = []
    for i in find(database, stub):
        i.pop('_id')
        new_stub.append(i)
    new_stub = new_stub[0]
    ce = new_stub['rasa_nlu_data']['common_examples']
    for i in find(MongoDB, common_examples):
        i.pop('_id')
        ce.append(i)
    new_stub = json.dumps(new_stub)
    f = open('/home/frtnx/grassroot-nlu/training_data.json', 'w')
    f.write(new_stub)
    auto_trainer()


def auto_trainer():
    print('\n\n')
    training_data = load_data('/home/frtnx/grassroot-nlu/training_data.json')
    trainer = Trainer(RasaNLUConfig('/home/frtnx/grassroot-nlu/config_mitie.json'))
    trainer.train(training_data)
    model_directory = trainer.persist('/home/frtnx/models')
    model = {'dir': model_directory}
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
    stored_model_score = '/home/frtnx/grassroot-nlu/current_model_score.txt'
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
        print('new model successfuly written')
        if model_directory:
            src = model_directory['dir']
            dest = '/home/frtnx/current_model/'
            if 'current_model' in os.listdir('/home/frtnx'):
                shutil.rmtree('/home/frtnx/current_model/')
            shutil.copytree(src,dest)
            print('new model successfuly generated. Ready for main script reinitialisation')
            new_model_checker.append(1) 
        else:
            print('No model specified')
    else:
        if model_directory:
            print("our new model isn't better than the one currently in use. Sustained.")

this_moment = "17:55"
  
schedule.every().day.at(this_moment).do(generate_training_data)

def start_training():
    schedule.run_pending()
    time.sleep(1)
    
