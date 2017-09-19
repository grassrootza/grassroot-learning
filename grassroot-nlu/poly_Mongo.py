from pymongo import MongoClient
client = MongoClient()
db = client.database
collection = db.collection
entries = db.entries
common_examples = db.common_examples
stub = db.stub
runtime_training_data = db.runtime_training_data


class MongoDB(object):
    def db_find(self, table):
        x = []
        for i in table.find():
            x.append(i)
        return x
    def db_find_one(self, table, key_val):
        return table.find_one(key_val)
    def db_insert_one(self, table, doc):
        table.insert_one(doc)

