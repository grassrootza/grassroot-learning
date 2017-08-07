from flask import Flask
from pymongo import MongoClient  # pymongo allows us to interact with our db
import uuid
import datetime

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
    archives.insert_one(instance) # sticks the recieved text+other info into our db
    # now send the text to our models and rasa    
      
@app.route('/')
def hello_world():
    return 'Here we will put some things!'


if __name__ == '__main__':
    app.run()

