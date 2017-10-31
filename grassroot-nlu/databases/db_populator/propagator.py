from __future__ import print_function
from common_examples import comex
from stub import black_hole
from pymongo import MongoClient
import pprint
import boto3
import json
import uuid
import datetime
import decimal

client = MongoClient()
db = client.test_database
collection = db.collection

stb = black_hole
ce = comex

def db_loader(database):
	database.load_db()


class mongodb:
    def load_db():
        stub = db.stub
        if stub.count() == 0:
            stub.insert_one(stb)
        common_examples = db.common_examples
        if common_examples.count() == 0:
            for e in ce:
                common_examples.insert_one(e)



class dynamoDb:
    def load_db():
        try:
            create_table('stub')
            create_new('stub', gen(stb, 'stb')) 
            create_table('common_examples')
            for e in ce:
                create_new('common_examples', gen(e, 'comex'))
        except Exception as e:
            print(e)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1', endpoint_url="https://dynamodb.eu-west-1.amazonaws.com")


def create_new(t_name, doc):
    table = dynamodb.Table(t_name)
    response = table.put_item(
        Item={
            'uid': doc['_id'],
            'text': doc['text'],
            'date': doc['date'],
            'past_lives': doc['past_lives']
             }
        )
    x = list(doc)
    if 'payload' in x:
        update(t_name, doc['_id'],doc['text'],doc['payload'])
    print("PutItem succeeded")
    return json.dumps(response, indent=4, cls=DecimalEncoder)       
 

def update(t_name, uid, text, p):
    table = dynamodb.Table(t_name)
    response = table.update_item(
        Key={
            'uid': uid,
            'text': text
        },
        UpdateExpression="set payload = :p",
        ExpressionAttributeValues={
            ':p': p
        },
        ReturnValues="UPDATED_NEW"
    )

    print("UpdateItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))


def create_table(name):
    table = dynamodb.create_table(
        TableName=name,
        KeySchema=[
            {
                'AttributeName': 'uid',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'text',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'uid',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'text',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )


def gen(doc, txt):                                                                        
    item = {                                                                         
            '_id': str(uuid.uuid4()),                                                
            'text': txt,                                               
            'date': str(datetime.datetime.now()),                                    
            'past_lives': [],                                                        
            'payload': doc                                                           
            }                                                                         
    return item 


# If you're in this file, it probably means you've broken something
# and are now desparately in search for possible bugs.
# Allow me then, a few words..

# How dare you touch my code!!
# You unworthy slave.

# May the bugs you create propagate into extinction.
# Mirroring the human race's trajectory.
# Annihilating themselves in some strange genetic algorithm
# And leaving you not knowing what the fuck

# May the world around you elude your understanding
# Causing an imbalance in your perception of space-time.

# And may you always find yourself out of every hole you find yourself in
# Perhaps even your grave. That would be so cool.
#                                      ~ FRTNX
