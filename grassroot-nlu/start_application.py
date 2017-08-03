from flask import Flask
from pymongo import MongoClient  # pymongo allows us to interact with our db

app = Flask(__name__)
client  = MongoClient() # assumes you have a mongod instance
                        # running on default host and port

db = client.test_database  # initialises our db, lazily.
collection = db.test_collection # initialises a table-like
                                # structure within our db

@app.route('/')
def hello_world():
    return 'Here we will put some things!'


if __name__ == '__main__':
    app.run()
