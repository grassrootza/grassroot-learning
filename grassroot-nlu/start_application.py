import os
import sys
import psutil
import logging


from flask import Flask,request, url_for, render_template
from config import interpreter, threshold, new_model_checker # runtime_training_data  # MongoDB table
import uuid, datetime
from duckling import Duckling
from databases.poly_database import *
from databases.poly_Mongo import *
from databases.poly_dynamo import *

from databases.db_helper import *

huidini = Duckling()
huidini.load()

app = Flask(__name__)
    
database = DynamoDB
MongoDB = 'optional database'

db_helper = DbMongo() # once properly built, changing this line will suffice to switch all methods

@app.route('/')
def index():
    if new_model_checker:
        restart_program()
    return render_template("textbox.html")


@app.route('/', methods=["POST"])
def parse():
    text_data = request.form['text']
    uid = request.form['uid']
    ret_val = process_identifier(text_data)
    if ret_val == True:   # what's going on here? type mixing with a boolean or a string? make it more intelligible
        request_data = {'text': text_data}
        user_bound = goldenGates(**request_data)
        data = user_bound['uid']
        return pep_talk("response.html",var1=str(user_bound), var2=data)
    elif ret_val == 'affirm':
        user_bound = "Your request is being processed..."
        save_as_training_instance(uid)
        return pep_talk("processing.html",var1=user_bound)
    elif ret_val == 'kamikaze':
        return render_template("textbox.html")
    elif ret_val == 'update':
        user_bound = transformer(text_data, uid)
        return str(user_bound)
    else:
        user_bound = osiris(ret_val, uid)
        return str(user_bound)


def process_identifier(text):
    x = interpreter.parse(text)
    value = x['intent']['name']
    if value == 'affirm':
        return value
    elif value == 'None':
        return 'update'
    elif value == 'negation':
        if x['entities'] != []: # any reason not to simplify to if [x'entities']:
            return x['entities'][0]['value']
        else:
            return 'kamikaze' # cute, not not maintainable, make it intelligible
    else:
        return True # rather return a string describing what case this is


def osiris(new_value, uid):
    try:
        old_text = db_helper.load_old_text(uid)
        new_text = old_text + " " + new_value # so here the problem is old_text might be nothing
        request_data = {'text': new_text}
        new_parsed = goldenGates(**request_data)
        if new_parsed['past_lives']:
            if new_parsed['past_lives'][0] != old_text:
                new_parsed['past_lives'].append(old_text)
        else:
            new_parsed['past_lives'].append(old_text)
        update_database(new_parsed)
        data = new_parsed['uid']
        return pep_talk("response.html", var1=new_parsed, var2=data)
    except:
        return "Patience and perseverence."


def transformer(text, uid):
    try:
        old_text = db_helper.load_old_text(uid)
        new_text = old_text+ " " + text
        request_data = {'text': new_text}
        new_parsed = goldenGates(**request_data)
        if new_parsed['past_lives'] != []:
            if new_parsed['past_lives'][0] != old_text:
                new_parsed['past_lives'].append(old_text)
        else:
            new_parsed['past_lives'].append(old_text)
        update_database(new_parsed) 
        data = new_parsed['uid']
        return pep_talk("response.html", var1=new_parsed, var2=data)
    except Exception as e:
        return str(e)


def pep_talk(template,var1=None, var2=None):
    return render_template(template, var1=var1, var2=var2) 


def goldenGates(**request_data):
    if database == MongoDB:                  
        recall = check_database(request_data['text'])
        if recall != False:
            return recall                            # suitable entry exists. Return said entry. Process complete.
    else:
        new_entry = {
                     'text': request_data['text'],
                     '_id' : str(uuid.uuid4()),
                     'date': str(datetime.datetime.now()),
                     'past_lives': []
                    }
        if database == MongoDB:
            insert_one(database, entries, new_entry)
        if database == DynamoDB:
            insert_one(database, 'entries', new_entry) # turn table names to strings when using dynamoDB
        uid = new_entry['_id']
        x = parser(new_entry['text'],uid,new_entry['date'],new_entry['past_lives']) 
        return x

def parser(text, uid, date_time,past_life):
    parse = interpreter.parse(text)
    parsed_data = {'parsed': parse, 'uid': uid, 'date': date_time, 'past_lives': past_life} 
    with open("./nsa/event_listener.txt", "a") as myfile:        
        myfile.write(str(parsed_data)+"\n\n")              
    res = update_database(parsed_data)
    parsed = time_formalizer(parse)
    parsed_data['parsed'] = parsed               
    return parsed_data

    
def update_database(new_data):
    if database == MongoDB:
        entries.update_one({'_id': new_data['uid']}, {"$set": new_data}, upsert=False)
        e = find_one(database, entries,{'_id': new_data['uid']})
        return str(e)
    if database == DynamoDB: 
        update('entries', new_data['uid'], new_data['parsed']['text'], str(new_data))
        e = find_one(database, 'entries', {'uid': new_data['uid']})
        return e

  
def check_database(text):
    previous_entry = find_one(database, entries,{'text': text})
    if previous_entry == None:
        return False
    else:
        self_confidence = previous_entry['parsed']['intent']['confidence']
        if self_confidence > threshold:
            return previous_entry
        else:
            return False


def save_as_training_instance(uid):
    if database == MongoDB:
        dirty = find_one(database, entries,{'uid': uid})
        cleansed = dirty['parsed']
        try:
            cleansed['intent'] = cleansed['intent']['name']
        except:
            pass
        if cleansed['entities'] != []:
            leng = len(cleansed['entities'])
            for i in range(0,leng):
                try:
                    item = cleansed['entities'][i]
                    item.pop('extractor')
                    item.pop('processors')
                except:
                    pass
        insert_one(database, runtime_training_data, cleansed)
    if database == DynamoDB:
        dirty = find_one(database, 'entries',{'uid': uid})[0]['payload']
        y = dirty.replace("'",'"')
        dirty = json.loads(y)
        cleansed = dirty['parsed']
        try:
            cleansed['intent'] = cleansed['intent']['name']
        except:
            pass
        if cleansed['entities'] != []:
            leng = len(cleansed['entities'])
            for i in range(0,leng):
                if cleansed['entities'][i]['entity'] != 'date_time':
                    try:
                        item = cleansed['entities'][i]
                        item.pop('extractor')
                        item.pop('processors')
                    except:
                        pass
                else:
                    return
            cleansed = {'_id': uid,
                        'text': 'runtime_training_data',
                        'date': str(datetime.datetime.now()),
                        'past_lives': [],
                        'payload': cleansed}
            insert_one(database, 'runtime_training_data', cleansed)
  
with app.test_request_context():
    print(url_for('parse', text='make your queries here'))


def time_formalizer(parsed_data):
    for i in range(0, len(parsed_data['entities'])):
        if parsed_data['entities'][i]['entity'] == 'date_time':
            value = parsed_data['entities'][i]['value']
            formal = formalizer_helper(value)
            parsed_data['entities'][i]['value'] = formal
    return parsed_data


def formalizer_helper(time_string):
    parsed = huidini.parse(time_string)
    for i in range(0,len(parsed)):
        if parsed[i]['dim'] == 'time':
            new_value = parsed[i]['value']['value']
            return new_value
  

def restart_program():
    try:
        p = psutil.Process(os.getpid())
        for i in p.open_files + p.connections:
            os.close(i.fd)
    except Exception as e:
        logging.error(e)
    python = sys.executable
    print("restarting...")
    new_model_checker.clear()
    os.execl(python,python, *sys.argv)


if __name__ == '__main__':
    app.run()

