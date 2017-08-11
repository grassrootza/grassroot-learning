from flask import Flask
from pymongo import MongoClient  # pymongo allows us to interact with our db
from rasa_nlu.model import Metadata, Interpreter
from rasa_nlu.config import RasaNLUConfig
import uuid, datetime

app = Flask(__name__)
client  = MongoClient() # assumes you have a mongod instance
                        # running on default host and port

db = client.test_database  # initialises our db, lazily.
collection = db.test_collection # initialises a table-like
                                # structure within our db
entries = db.entries

def giveme(text):
    instance = {'text':text,
                'date':datetime.datetime.utcnow(),
                '_id':uuid.uuid4(),
                'model_found':None
               }
    entries.insert_one(instance) # sticks the recieved text+other info into our db
    metadata = Metadata.load('/path/to/model_directory')
    interpreter = Interpreter.load(metadata, RasaNLUConfig('/path/to/config_mitie.json'))
    result = interpreter.parse(text) # returns a dict/json-like object parsed by rasa. 
      
@app.route('/parse')
def parse():
    text = request.args.get('text','')
    giveme(text)
    
with app.test_request_context():
    print(url_for('parse', text='make your queries here'))

if __name__ == '__main__':
    app.run()

