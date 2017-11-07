from flask import Flask,request, url_for, render_template
from config import interpreter, database
import uuid, time, datetime, pprint
from duckling import Duckling
from databases.poly_database import *
from databases.poly_Mongo import *
from databases.poly_dynamo import *
import os
import sys
import psutil
import logging


app = Flask(__name__)
    

@app.route('/')
def index():
    return render_template("textbox.html")


@app.route('/', methods=["POST"])
def parse():
    text_data = request.form['text']
    uid = request.form['uid']
    ret_val = process_identifier(text_data)
    if ret_val == 'new_entry':   
        request_data = {'text': text_data}
        user_bound = goldenGates(**request_data)
        data = user_bound['uid']
        return pep_talk("response.html",var1=str(user_bound), var2=data)
    elif ret_val == 'affirm':
        user_bound = "Your request is being processed..."
        save_as_training_instance(uid)
        return pep_talk("processing.html",var1=user_bound)
    elif ret_val == 'reset':
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
        if x['entities']  != []:
            return x['entities'][0]['value']
        else:
            return 'reset'
    else:
        return 'new_entry'


def osiris(new_value, uid):
    try:
        old_text = load_old_text(database, {'uid':uid})
        new_text = old_text + " " + new_value
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
    except:
        return "Patience and perseverence."


def transformer(text, uid):
    try:
        entry = find_previous_entry(database, {'uid':uid})
        old_text = entry['text']
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
    recall = check_database(database, request_data['text'])
    if recall != False:
        return recall                            # suitable entry exists. Return said entry. Process complete.
    else:
        new_entry = {
                     'text': request_data['text'],
                     '_id' : str(uuid.uuid4()),
                     'date': str(datetime.datetime.now()),
                     'past_lives': []
                    }
        insert_one(database, new_entry)
        uid = new_entry['_id']
        x = parser(new_entry['text'],uid,new_entry['date'],new_entry['past_lives']) 
        return x

def parser(text, uid, date_time,past_life):
    parse = interpreter.parse(text)
    parsed_data = {'parsed': parse, 'uid': uid, 'date': date_time, 'past_lives': past_life} 
    with open("./nsa/event_listener.txt", "a") as myfile:        
        myfile.write(str(parsed_data)+"\n\n")              
    res = update_database(parsed_data)
    print('This is what I have put in the database', parsed_data)
    parsed = time_formalizer(parse)
    parsed_data['parsed'] = parsed               
    return parsed_data

    
def update_database(new_data):
    update_db(database, new_data)


def save_as_training_instance(uid):
    find_clean_and_save(database, {'uid': uid})
  
with app.test_request_context():
    print(url_for('parse', text='make your queries here'))


houdini = Duckling()
houdini.load()

def time_formalizer(parsed_data):
    for i in range(0, len(parsed_data['entities'])):
        if parsed_data['entities'][i]['entity'] == 'date_time':
            value = parsed_data['entities'][i]['value']
            formal = formalizer_helper(value)
            parsed_data['entities'][i]['value'] = formal
    return parsed_data


def formalizer_helper(time_string):
    parsed = houdini.parse(time_string)
    for i in range(0,len(parsed)):
        if parsed[i]['dim'] == 'time':
            new_value = parsed[i]['value']['value']
            return new_value
  


if __name__ == '__main__':
    app.run(host='0.0.0.0')
