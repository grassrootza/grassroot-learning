import os
try:
    os.system('rm logs/*')
except:
    pass
    
import threading
from logger import *

def displayLogs():
    """tails the log file"""
    os.system("tail -f logs/nlu.log")

threading.Thread(target=displayLogs).start()

rootLogger.info('Ignition.')
import os
import sys
import requests
import logging
import uuid
import time
import datetime
from flask import Flask, request, url_for, render_template, Response

from config import intent_interpreter, vote_interpreter, group_interpreter, todo_interpreter, \
            meeting_interpreter, updates_interpreter, database
from databases.poly_database import *
from databases.poly_Mongo import *
from databases.poly_dynamo import *

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the home page."""
    return render_template("textbox.html")


# emulator/tester
# @app.route('/', methods=["POST"])
# def parse_view():
#     Main entry point. Requires a POST call 
#     text_data = request.form['text']
#     uid = request.form['uid']
#     ret_val = process_identifier(text_data)
# 
#     if ret_val == 'new_entry':
#         user_bound = process_gateway(text_data)
#         data = user_bound['uid']
#         return render_html_template("response.html",var1=json.dumps(user_bound['parsed']), var2=data)
# 
#     elif ret_val == 'affirm':
#         user_bound = "Your request is being processed..."
#         save_as_training_instance(uid)
#         return render_html_template("processing.html",var1=user_bound)
# 
#     elif ret_val == 'reset':
#         return render_template("textbox.html")
# 
#     elif ret_val == 'update':
#         new_parsed = add_detail_to_text(text_data, uid)
#         return render_html_template("response.html", var1=json.dumps(new_parsed['parsed']), var2=new_parsed['uid'])
# 
#     else:
#         user_bound = add_detail_to_previous_text_state(ret_val, uid)
#         return str(user_bound)


# REST method
@app.route('/parse')
def parse_rest():
    """Main entry point. API path is '/parse?text=query', where query is the text you want parsed."""
    text_data = request.args.get('text')
    uid = request.args.get('uid')
    rootLogger.debug("received a parse request.\ntext: %s\nuid: %s" % (text_data, uid))
    destiny = process_identifier(text_data)
    rootLogger.debug("Request is destined to '%s'" % destiny)

    if destiny == 'new_entry':
        entity_to_return = process_gateway(text_data)
        rootLogger.debug("returning entity 2: " + "\n" + json.dumps(entity_to_return, indent=1))
        return app.response_class(json.dumps(entity_to_return), content_type='application/json')

    elif destiny == 'update':
        entity_to_return = add_detail_to_text(text_data, uid)
        rootLogger.debug("returning entity: " + "\n" + json.dumps(entity_to_return, indent=1))
        return app.response_class(json.dumps(entity_to_return), content_type='application/json')

    elif destiny == 'reset':
        return render_template("textbox.html")

    # elif destiny == 'update':
    #     new_parsed = add_detail_to_text(text_data, uid)
    #     return render_html_template("response.html", var1=json.dumps(new_parsed['parsed']), var2=new_parsed['uid'])

    else:
        entity_to_return = process_gateway(text_data)
        rootLogger.debug("returning entity 2: " + "\n" + json.dumps(entity_to_return, indent=1))
        return app.response_class(json.dumps(entity_to_return), content_type='application/json')


# for tests
@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server :(')
    func()
    return 'Server shutting down'


def process_identifier(text):
    """Identifies where a process will go. This process produces a certain amount of
    redundancy and is most like to change or be deprecated soon."""
    x = intent_interpreter.parse(text)
    value = x['intent']['name']
    if value == 'affirm':
        return value
    elif value == 'update':
        return 'update'
    elif value == 'negate':
        if x['entities']  != []:
            return x['entities'][0]['value']
        else:
            return 'reset'
    else:
        return 'new_entry'


def add_detail_to_previous_text_state(new_value, uid):
    """Called when a process is identified with the 'update' intent.
    searches database for text with uid and appends new_value to it. It
    then sends it for parsing and returns output"""
    try:
        old_text = load_old_text(database, {'uid':uid})
        new_text = old_text + " " + new_value
        new_parsed = process_gateway(new_text)

        if new_parsed['past_lives'] != []:

            if new_parsed['past_lives'][0] != old_text:
                new_parsed['past_lives'].append(old_text)

        else:
            new_parsed['past_lives'].append(old_text)

        update_database(new_parsed)
        data = new_parsed['uid']

        return render_html_template("response.html", var1=json.dumps(new_parsed['parsed']), var2=data)

    except Exception as e:
        rootLogger.debug(str(e))
        return "Ooops. Looks like the application's misbehaved. A report has been issued to its creators."
        # notify() # proposed email service that notifies developers about errors in real time.
        # the idea here is that the less emails you recieve, the better. Bad code will blow up your phone
        # like a toll free hotline.
        # A single gmail account will suffice per organisation. Pass login info on container start up



def add_detail_to_text(text, uid):
    """Called when a process is identified with the 'update' intent.
    searches database for text with uid and appends new_value to it. It
    then sends it for parsing and returns output"""
    try:
        entry = find_previous_entry(database, {'uid':uid})
        old_text = entry['text']
        new_text = old_text+ " " + text
        new_parsed = process_gateway(new_text)

        if new_parsed['past_lives'] != []:

            if new_parsed['past_lives'][0] != old_text:
                new_parsed['past_lives'].append(old_text)
        else:
            new_parsed['past_lives'].append(old_text)

        update_database(new_parsed)
        return new_parsed

    except Exception as e:
        rootLogger.debug(str(e))
        return "Ooops. Looks like the application's misbehaved. A report has been issued to its creators."
        # notify() # proposed email service that notifies developers about errors in real time.
        # the idea here is that the less emails you recieve, the better. Bad code will blow up your phone
        # like a toll free hotline.
        # A single gmail account will suffice per organisation. Pass login info on container start up


def render_html_template(template,var1=None, var2=None):
    return render_template(template, var1=var1, var2=var2)


purgables = ["extractor"]


def process_gateway(text_to_parse):
    """This function is responsible for assigning uids to new texts and saving text to db,
    sending them for parsing and returning them. Before parsing it will
    check database for requested text and if it already exists it is returned."""
    recall = check_database(database, text_to_parse)
    if recall != False:
        return recall   # suitable entry exists. Return said entry. Process complete.
    else:
        new_entry = {
                     'text': text_to_parse,
                     '_id' : str(uuid.uuid4()),
                     'date': str(datetime.datetime.now()),
                     'past_lives': []
                    }

        insert_one(database, new_entry)

        uid = new_entry['_id']
        x = parser(new_entry['text'], uid, new_entry['date'], new_entry['past_lives'])
        return x


def parser(text, uid, date_time, past_life):
    """This function handles the nlu parsing. It first extracts intent and
    if nature of intent requires entity extraction the text is then parsed 
    by a secondary extractor. It also formalises informal datetime strings
    """
    intent_raw = intent_interpreter.parse(text)
    intent = intent_raw['intent']['name']
    if intent == 'call_meeting':
        parse = meeting_interpreter.parse(text)
    elif intent == 'call_vote':
        parse = vote_interpreter.parse(text)
    elif 'todo' in intent:
        parse = todo_interpreter.parse(text)
    elif intent == 'create_group':
        parse = group_interpreter.parse(text)
    else:
        parse = intent_raw 

    parsed_data = {'parsed': parse, 'uid': uid, 'date': date_time, 'past_lives': past_life}
    res = update_database(parsed_data)
    parsed = time_formalizer(parse)
    parsed_data['parsed'] = parsed
    if parsed_data['parsed']['entities'] != []:
        for i in range(0,len(parsed_data['parsed']['entities'])):
            if "extractor" in parsed_data['parsed']['entities'][i]:
                parsed_data['parsed']['entities'][i].pop('extractor')
    return parsed_data


def update_database(new_data):
    """updates database with new_data from parser. This is the database
    process_gateway() searches for past entries that are suitable to be returned"""
    update_db(database, new_data)


def save_as_training_instance(uid):
    """Turns all affirmed parsed values into training data.""" 
    find_clean_and_save(database, {'uid': uid})

def time_formalizer(parsed_data):
    """Formalises datetime values recieved from parser() by extracting target value from parsed
    text and sending it to formalizer_helper()"""
    for i in range(0, len(parsed_data['entities'])):
        if parsed_data['entities'][i]['entity'] == 'datetime':
            value = parsed_data['entities'][i]['value']
            formal = formalizer_helper(value)
            parsed_data['entities'][i]['value'] = formal
    return parsed_data


def formalizer_helper(time_string):
    """time_formalizer's helper. Responsible for sending out api requests"""
    return requests.get('http://learning.grassroot.cloud/datetime?date_string=%s' % time_string).content.decode('ascii')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
