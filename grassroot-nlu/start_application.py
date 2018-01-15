from flask import Flask,request, url_for, render_template, Response
from config import interpreter, database
import uuid, time, datetime, pprint
from duckling import Duckling
from databases.poly_database import *
from databases.poly_Mongo import *
from databases.poly_dynamo import *
from distance import *
import os
import sys
import psutil
import logging
import json


app = Flask(__name__)

d = Duckling()
d.load()
    

@app.route('/')
def index():
    return render_template("textbox.html")


# emulator/tester
@app.route('/', methods=["POST"])
def parse_view():
    text_data = request.form['text']
    uid = request.form['uid']
    ret_val = process_identifier(text_data)

    if ret_val == 'new_entry':   
        user_bound = goldenGates(text_data)
        data = user_bound['uid']
        return pep_talk("response.html",var1=json.dumps(user_bound['parsed']), var2=data)

    elif ret_val == 'affirm':
        user_bound = "Your request is being processed..."
        save_as_training_instance(uid)
        return pep_talk("processing.html",var1=user_bound)

    elif ret_val == 'reset':
        return render_template("textbox.html")

    elif ret_val == 'update':
        new_parsed = transformer(text_data, uid)
        return pep_talk("response.html", var1=json.dumps(new_parsed['parsed']), var2=new_parsed['uid'])

    else:
        user_bound = osiris(ret_val, uid)
        return str(user_bound)


# REST method
@app.route('/parse')
def parse_rest():
    text_data = request.args.get('text')
    uid = request.args.get('uid')

    print("received a parse request, text = " + text_data)

    ret_val = process_identifier(text_data)
    print("return type = " + ret_val)

    if ret_val == 'new_entry':
        entity_to_return = goldenGates(text_data)
        print("returning entity 2: " + "\n" + json.dumps(entity_to_return, indent=1))      
        return app.response_class(json.dumps(entity_to_return), content_type='application/json')

    elif ret_val == 'update':
        entity_to_return = transformer(text_data, uid)
        print("returning entity: " + "\n" + json.dumps(entity_to_return, indent=1))
        return app.response_class(entity_to_return, content_type='application/json')

    else:
        return "Error, didn't know what to do"


@app.route('/datetime')
def date():

    d_string = request.args.get('date_string')

    x = d.parse(d_string)
    x = x[len(x)-1]
    return Response(x['value']['value'][:16], mimetype='application/json')
    


@app.route('/distance')
def w_distance():

    text = request.args.get('text').lower().strip()
    return Response(json.dumps(distance(text)), mimetype='application/json')



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
        new_parsed = goldenGates(new_text)

        if new_parsed['past_lives'] != []:

            if new_parsed['past_lives'][0] != old_text:
                new_parsed['past_lives'].append(old_text)

        else:
            new_parsed['past_lives'].append(old_text)

        update_database(new_parsed)
        data = new_parsed['uid']

        return pep_talk("response.html", var1=json.dumps(new_parsed['parsed']), var2=data)

    except:
        return "Patience and perseverence."


def transformer(text, uid):

    try:

        entry = find_previous_entry(database, {'uid':uid})
        old_text = entry['text']
        new_text = old_text+ " " + text
        new_parsed = goldenGates(new_text)

        if new_parsed['past_lives'] != []:

            if new_parsed['past_lives'][0] != old_text:
                new_parsed['past_lives'].append(old_text)

        else:
            new_parsed['past_lives'].append(old_text)

        update_database(new_parsed) 
        return new_parsed

    except Exception as e:
        return str(e)


def pep_talk(template,var1=None, var2=None):
    return render_template(template, var1=var1, var2=var2) 


purgables = ["extractor"]


def goldenGates(text_to_parse):
    recall = check_database(database, text_to_parse)

    if recall != False:
        return recall  
                                  # suitable entry exists. Return said entry. Process complete.
    else:
        new_entry = {
                     'text': text_to_parse,
                     '_id' : str(uuid.uuid4()),
                     'date': str(datetime.datetime.now()),
                     'past_lives': []
                    }

        insert_one(database, new_entry)

        uid = new_entry['_id']
        x = parser(new_entry['text'],uid,new_entry['date'],new_entry['past_lives']) 
        return x


def parser(text, uid, date_time, past_life):
    parse = interpreter.parse(text)
    parsed_data = {'parsed': parse, 'uid': uid, 'date': date_time, 'past_lives': past_life} 

    with open("./nsa/event_listener.txt", "a") as myfile:        
        myfile.write(str(parsed_data)+"\n\n")

    res = update_database(parsed_data)
    parsed = time_formalizer(parse)
    parsed_data['parsed'] = parsed

    if parsed_data['parsed']['entities'] != []:

        for i in range(0,len(parsed_data['parsed']['entities'])):

            if "extractor" in parsed_data['parsed']['entities'][i]:
                parsed_data['parsed']['entities'][i].pop('extractor') 

    return parsed_data

    
def update_database(new_data):
    update_db(database, new_data)


def save_as_training_instance(uid):
    find_clean_and_save(database, {'uid': uid})
  
#with app.test_request_context():
#    print(url_for('parse', text='make your text queries here'))

d = Duckling()
d.load()

def time_formalizer(parsed_data):

    for i in range(0, len(parsed_data['entities'])):

        if parsed_data['entities'][i]['entity'] == 'date_time':
            value = parsed_data['entities'][i]['value']
            formal = formalizer_helper(value)
            parsed_data['entities'][i]['value'] = formal

    return parsed_data


def formalizer_helper(time_string):
    parsed = d.parse(time_string)

    for i in range(0,len(parsed)):
        
        if parsed[i]['dim'] == 'time':
            new_value = parsed[i]['value']['value']
            return new_value
  


if __name__ == '__main__':
    app.run()
