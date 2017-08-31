from flask import Flask,request, url_for, render_template
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
metadata = Metadata.load('/home/frtnx/models/model_20170831-114540') #store these in a config file. no need to expose ourfiile system
interpreter = Interpreter.load(metadata, RasaNLUConfig('/home/frtnx/anaconda3/lib/python3.6/site-packages/rasa_nlu/config_mitie.json'))

#process management
timer = []

app = Flask(__name__)

def process_identifier(text):
    x = interpreter.parse(text)
    value1 = x['intent']['name']
    value2 = x['entities']
    if value1 == 'affirm':
        return 'affirm'
    else:
        if value1 == 'None':
            return 'update'
        else:
            return True

@app.route('/')
def my_form():
    return render_template("textbox.html")

@app.route('/', methods=["POST"])
def parse():
    text_data = request.form['text']
    uid = request.form['uid']
    #return str(text_data)
    prcss = process_identifier(text_data)
    x = None
    if prcss == True:   
        request_data = {'text': text_data}
        x = identifier(**request_data) #which returns parsed data + uid + date
        datap = x['parsed']['text']
        data = [datap]
        return NQoutput("response.html",var1=str(x), var2=data)
    elif prcss == 'affirm':
        x = "Your request is being processed..."
        return NQoutput("processing.html",var1=x)
    else:
        x = transformer(text_data, uid)
        return str(x)

def transformer(text, uid):
    try:
        Uid = []
        for i in uid:
            if i != '[' and i != ']' and i != "'":
                Uid.append(i)
        uidd = ''.join(Uid)
        x = entries.find_one({'text': uidd})
        old_text = x['text']
        new_text = old_text+ " " + text
        request_data = {'text': new_text}
        new_parsed = identifier(**request_data)
        return NQoutput("response.html", var1=new_parsed, var2=new_text)
    except:
        return str(uidd)


def NQoutput(template,var1=None, var2=None):
    return render_template(template, var1=var1, var2=var2) 

def identifier(**request_data):                  # request debuts here
    #start = time.time()
    #timer.append(start)
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
    #end = time.time()
    #timer.append(end)
    #process_time = timer[1] - timer[0]
    #timer.clear()
    parsed_data = {'parsed': parsed, 'uid': uid, 'date': date_time} # insert process time here
    with open("event_listener.txt", "a") as myfile:        
        myfile.write(str(parsed_data)+"\n\n")              
    res = update_database(parsed_data)               
    #parsed_data.pop('process_time')
    return parsed_data                                 # rabbit hole we go. I find the return process beautiful.
    
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
   
