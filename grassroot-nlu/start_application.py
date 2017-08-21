from flask import Flask,request, url_for
import pymongo
from pymongo import MongoClient
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Interpreter, Metadata
import uuid, time, datetime, pprint

# Mongo Settup
client = MongoClient()
db = client.database
collection = db.collection
entries = db.entries

#Rasa Settup
metadata = Metadata.load('/home/frtnx/models/model_20170816-092910')
interpreter = Interpreter.load(metadata, RasaNLUConfig('/home/frtnx/anaconda3/lib/python3.6/site-packages/rasa_nlu/config_mitie.json'))

#process management
timer = []

app = Flask(__name__)

@app.route('/parse')
def parse():
    text_data = request.args.get('text','')
    request_data = {'text': text_data}
    x = identifier(**request_data) #which returns parsed data + uid + date
    return x 


def identifier(**request_data):                  # request debuts here
    start = time.time()
    timer.append(start)
    recall = check_database(request_data['text'])
    if recall != False:
        return recall                            # suitable entry exists. Return said entry. Process complete.
    else:
        new_entry = {
                     'text': request_data['text'],
                     '_id' : uuid.uuid4(),
                     'date': str(datetime.datetime.utcnow())
	                }
        entries.insert_one(new_entry)
        uid = new_entry['_id']
        x = parser(new_entry['text'],uid,new_entry['date']) # down the
        return x

def parser(text, uid, date_time):
    parsed = interpreter.parse(text)
    end = time.time()
    timer.append(end)
    process_time = timer[1] - timer[0]
    timer.clear()
    parsed_data = {'parsed': parsed, 'uid': uid, 'date': date_time,'process_time': process_time}
    with open("event_listener.txt", "a") as myfile:        
        myfile.write(str(parsed_data)+"\n\n")              
    res = update_database(parsed_data)               
    parsed_data.pop('process_time')
    return str(parsed_data)                                 # rabbit hole we go. I find the return process beautiful.
    
def update_database(new_data):
    entries.update_one({'_id': new_data['uid']}, {"$set": new_data}, upsert=False)
    e = entries.find_one({'_id': new_data['uid']})
    return str(e)
  
def check_database(text):
    previous_entry = entries.find_one({'text': text})
    if previous_entry == None:
        return False
    else:
        self_confidence = previous_entry['parsed']['intent']['confidence']
        if self_confidence > 0.4:
            return str(previous_entry)
        else:
            return False
  
with app.test_request_context():
    print(url_for('parse', text='make your queries here'))

if __name__ == '__main__':
    app.run()
   
