from __future__ import print_function
import boto3
import json
import decimal
from boto3.dynamodb.conditions  import Key, Attr
from botocore.exceptions import ClientError


class DynamoDB(object):
    def db_find(self, table):
        x = []
        for i in table.find():
            x.append(i)
        return x
    def db_find_one(self, table, key_val):
        val = key_val['uid']
        return ddb_find(table, val)
    def db_insert_one(self, table, doc):
        create_new(table, doc)


#Helper class to convert a DynamoDB item to json
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")


def create_new(t_name, doc):
    table = dynamodb.Table(t_name)
    #if t_name == 'entries':
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
