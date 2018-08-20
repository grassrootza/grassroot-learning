import os
try:
    os.system('rm logs/*')
except:
    pass
    
import threading
from logger import *
rootLogger.info('Ignition.')

def logdog():
    """tails the log file"""
    os.system("tail -f logs/nlu.log")

def logmouse():    
    requests = open('logs/requests.txt', 'a')
    requests.close()    
    os.system('python request_logger.py')

def logowl():
    file = open('logs/overflowBlock', 'w')
    file.write('0')
    file.close()     
    os.system('python overflow_handler.py')    

threading.Thread(target=logdog).start()
threading.Thread(target=logmouse).start()
threading.Thread(target=logowl).start()

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
from mail_service import mail

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the home page."""
    return render_template("textbox.html")


# REST method
@app.route('/parse')
def parse_rest():
    """Main entry point. API path is '/parse?text=query', where query is the text you want parsed."""
    try:
        text_data = request.args.get('text')
        uid = request.args.get('uid')
        rootLogger.debug("Received parse request: { text: %s, uid: %s }" % (text_data, uid))
        current_files = os.listdir('./')
        if 'sysf.txt' in current_files:
            # do_the_thing(text_data)
            err_message = "System is down for maintenance. Please try again in an hour."
            return app.response_class(json.dumps({ 'err': '%s' } % err_message), content_type='application/json')        
        destiny = process_identifier(text_data)
        rootLogger.debug("Request is destined for '%s'" % destiny)
    
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

        else:
            entity_to_return = process_gateway(text_data)
            rootLogger.debug("returning entity 2: " + "\n" + json.dumps(entity_to_return, indent=1))
            return app.response_class(json.dumps(entity_to_return), content_type='application/json')
    except Exception as e:
        rootLogger.error(str(e))
        mail('Error in main.py, parse_rest() %s' % str(e), 'Error')


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
            return app.response_class(json.dumps(x), content_type='application/json')
    else:
        return 'new_entry'


def add_detail_to_text(text, uid, *prev_text_state):
    """Called when a process is identified with the 'update' intent.
    searches database for text with uid and appends new_value to it. It
    then sends it for parsing and returns output"""
    try:
        if prev_text_state:
            old_text = load_old_text(database, {'uid':uid})
        else:
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
        rootLogger.error(str(e))
        mail(str(e), 'Error')
        return "Ooops. Looks like the application's misbehaved. A report has been issued to its creators."


def render_html_template(template,var1=None, var2=None):
    return render_template(template, var1=var1, var2=var2)


purgables = ["extractor"]


def process_gateway(text_to_parse):
    """This function is responsible for assigning uids to new texts and saving text to db,
    sending them for parsing and returning them. Before parsing it will
    check database for requested text and if it already exists it is returned."""
    try:
        # recall = check_database(database, text_to_parse)
        recall = False
        if recall != False:
            if recall['parsed']['intent']['confidence'] < 0.5:
                do_the_thing('%s' % text_to_parse)
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
    except Exception as e:
        rootLogger.error(str(e))
        mail('An error was encountered in main.py: process_gateway() %s' % str(e), 'Error')


def parser(text, uid, date_time, past_life):
    """This function handles the nlu parsing. It first extracts intent and
    if nature of intent requires entity extraction the text is then parsed 
    by a secondary extractor. It also formalises informal datetime strings
    """
    try:
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
    
        if parse['intent']['confidence'] < 0.5:
            do_the_thing('%s' % text)

        parsed_data = {'parsed': parse, 'uid': uid, 'date': date_time, 'past_lives': past_life}
        res = update_database(parsed_data)
        parsed = time_formalizer(parse)
        parsed_data['parsed'] = parsed
        if parsed_data['parsed']['entities'] != []:
            for i in range(0,len(parsed_data['parsed']['entities'])):
                if "extractor" in parsed_data['parsed']['entities'][i]:
                    parsed_data['parsed']['entities'][i].pop('extractor')
        return parsed_data
    except Exception as e:
        rootLogger.error(str(e))
        mail('An error occured in main.py: parser() %s' % str(e), 'Error')

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
    try:
        for i in range(0, len(parsed_data['entities'])):
            if parsed_data['entities'][i]['entity'] == 'datetime':
                value = parsed_data['entities'][i]['value']
                formal = formalizer_helper(value)
                parsed_data['entities'][i]['value'] = formal
        return parsed_data
    except Exception as e:
        rootLogger.error(e)
        mail('An error occured in main.py: time_formalizer() %s' % str(e), 'Error')


def formalizer_helper(time_string):
    """time_formalizer's helper. Responsible for sending out api requests"""
    return requests.get('http://learning.grassroot.cloud/datetime?date_string=%s' % time_string).content.decode('ascii')

def do_the_thing(text):
    requests = open('logs/requests.txt', 'a')
    requests.write(text+'\n')
    requests.close()    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
