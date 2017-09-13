from flask import Flask,request, url_for, render_template
import pymongo
from config import interpreter, entries
import uuid, time, datetime, pprint
from duckling import Duckling
huidini = Duckling()
huidini.load()

app = Flask(__name__)

def process_identifier(text):
    x = interpreter.parse(text)
    value = x['intent']['name']
    if value == 'affirm':
        return 'affirm'
    else:
        if value == 'None':
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
    prcss = process_identifier(text_data)
    x = None
    if prcss == True:   
        request_data = {'text': text_data}
        x = identifier(**request_data)
        data = x['uid']
        return NQoutput("response.html",var1=str(x), var2=data)
    elif prcss == 'affirm':
        x = "Your request is being processed..."
        return NQoutput("processing.html",var1=x)
    else:
        x = transformer(text_data, uid)
        return str(x)

def transformer(text, uid):
    try:
        x = entries.find_one({'uid': uid})
        old_text = x['text']
        new_text = old_text+ " " + text
        request_data = {'text': new_text}
        new_parsed = identifier(**request_data)
        new_parsed['past_lives'].append(old_text)
        update_database(new_parsed) 
        data = new_parsed['uid']
        return NQoutput("response.html", var1=new_parsed, var2=data)
    except:
        return "I'm not buying it"


def NQoutput(template,var1=None, var2=None):
    return render_template(template, var1=var1, var2=var2) 

def identifier(**request_data):                  
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
        entries.insert_one(new_entry)
        uid = new_entry['_id']
        x = parser(new_entry['text'],uid,new_entry['date'],new_entry['past_lives']) # down the
        return x

def parser(text, uid, date_time,past_life):
    parse = interpreter.parse(text)
    parsed = time_formalizer(parse)
    parsed_data = {'parsed': parsed, 'uid': uid, 'date': date_time, 'past_lives': past_life} # insert process time here
    with open("event_listener.txt", "a") as myfile:        
        myfile.write(str(parsed_data)+"\n\n")              
    res = update_database(parsed_data)               
    return parsed_data
    #return res                                 # rabbit hole we go. I find the return process beautiful.
    
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
            return previous_entry
        else:
            return False
  
with app.test_request_context():
    print(url_for('parse', text='make your queries here'))

def render_sidebar_template(tmpl_name, **kwargs):
    (var1,var2,var3) = generate_sidebar_data()
    return render_template(tmpl_name, var1=var1, var2=var2, var3=var3, **kwargs)

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


if __name__ == '__main__':
    app.run()
   
