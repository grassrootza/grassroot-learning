from abc import ABCMeta
from abc import abstractmethod

from pymongo import MongoClient


class DbHelper:
    __metaclass__ = ABCMeta

    @abstractmethod
    def load_old_text(self, uid):
        """Retrieve old text stored under this UID, if it exists"""
        pass


class DbMongo(DbHelper):
    def __init__(self):
        print("Initiating Mongo DB Helper")
        client = MongoClient()
        db = client.database
        collection = db.collection
        entries = db.entries
        common_examples = db.common_examples
        stub = db.stub
        runtime_training_data = db.runtime_training_data

    def load_old_text(self, uid):
        return entries.find_one({'uid': uid})['past_lives'][0]


class DbDynamo(DbHelper):
    def __init__(self):
        print("Initiating DynamoDB Helper")

    def load_old_text(self, uid):
        # stashing it here, though use boto instead of handrolling
        #x = find_one(database, 'entries', {'uid': uid})[0]['payload']
        #y = x.replace("'", '"')
        #x = json.loads(y)
        #old_text = x['past_lives'][0]
        return "to complete"


if __name__ == '__main__':
    print('Mongo subclass: ', issubclass(DbMongo, DbHelper))
    print('Mongo instance: ', isinstance(DbMongo(), DbHelper))

    print('Dynamo subclass: ', issubclass(DbDynamo, DbHelper))
    print('Dynamo instance: ', isinstance(DbDynamo(), DbHelper))

