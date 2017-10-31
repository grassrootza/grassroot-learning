from __future__ import print_function
import boto3
import json
import decimal
from boto3.dynamodb.conditions  import Key, Attr
from botocore.exceptions import ClientError
import re


class DynamoDB(object):
    def db_find(self, table):
        x = []
        for i in table.find():
            x.append(i)
        return x
    def db_find_one(self, table, key_val):
        val = key_val['uid']
        return ddb_find(table, val)
    def db_insert_one(self, doc):
        create_new('entries', doc)
    def load_old_Text(self, key_val):
        x = ddb_find('entries',key_val['uid'])[0]['payload']
        y = str_to_dict(x)
        old_text = y['past_lives'][0]
        return old_text
    def find_previous_Entry(self, key_val):
        return ddb_find('entries',key_val['uid'])[0]
    def find_clean_save(self, key_val):
        clean_and_save(key_val['uid'])
    def update_DB(self, doc):
        update('entries', doc['uid'], doc['parsed']['text'], str(doc))
        e = ddb_find('entries', doc['uid'])
        return e
    def check_db(self, text):
        table = dynamodb.Table('entries')
        entries = table.scan()['Items']
        for entry in entries:
            if entry['text'] == text:
                payload = entry['payload']
                entry = str_to_dict(payload)
                if entry['parsed']['intent']['confidence'] > 0.6:
                    return entry
        return False



#Helper class to convert a DynamoDB item to json
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1', endpoint_url="http://localhost:8000") # endpoint_url="https://dynamodb.eu-west-1.amazonaws.com")

def str_to_dict(string):
    x = string.replace("'",'"')
    return json.loads(x) 


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


def get(t_name, uid):
    table = dynamodb.Table(t_name)
    try:
        response = table.get_item(
            Key={
                'year': year,
                'title': title
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        print("GetItem succeeded:")
        x = json.dumps(item, indent=4,cls=DecimalEncoder)
        the_dict = json.loads(x)
        return the_dict


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

    print("Table status:", table.table_status)


def ddb_find(t_name, value):
    table = dynamodb.Table(t_name)
    response = table.query(
        KeyConditionExpression=Key('uid').eq(value)
    )

    return response['Items']


def delete_table(table_name):
    table = dynamodb.Table(table_name)
    table.delete()


def clean_and_save(uid):
    dirty = ddb_find('entries',uid)[0]['payload']
    y = dirty.replace("'",'"')
    dirty = json.loads(y)
    cleansed = dirty['parsed']
    try:
        cleansed['intent'] = cleansed['intent']['name']
    except:
        pass
    if cleansed['entities'] != []:
        leng = len(cleansed['entities'])
        for i in range(0,leng):
            if cleansed['entities'][i]['entity'] != 'date_time':
                try:
                    item = cleansed['entities'][i]
                    item.pop('extractor')
                    item.pop('processors')
                except:
                    pass
            else:
                date_str = cleansed['entities'][i]['value']
                match = re.search(r'(\d+-\d+-\d+T)', date_str)
                if match:
                    return "value contains suboptimal formats. Instance not saved in training data."
        cleansed = {'_id': uid,
                    'text': 'runtime_training_data',
                    'date': str(datetime.datetime.now()),
                    'past_lives': [],
                    'payload': cleansed}
        create_new('runtime_training_data', cleansed)


try:
    create_table('entries')
except:
    pass

try:
    create_table('runtime_training_data')
except:
    pass
    