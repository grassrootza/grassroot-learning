from pymongo import MongoClient
client = MongoClient()
db = client.database
collection = db.collection
entries = db.entries
common_examples = db.common_examples
stub = db.stub
runtime_training_data = db.runtime_training_data

threshold = 0.7

class MongoDB(object):
    def db_find(self, table):
        x = []
        for i in table.find():
            x.append(i)
        return x
    def db_find_one(self, table, key_val):
        return table.find_one(key_val)
    def db_insert_one(self, doc):
        entries.insert_one(doc)
    def load_old_Text(self, uid):
        x = entries.find_one(uid)
        old_text = x['past_lives'][0]
        return old_text
    def find_previous_Entry(self, uid):
    	return entries.find_one(uid)
    def find_clean_save(self, uid):
    	clean_and_save(uid)
    def update_DB(self, doc):
        entries.update_one({'_id': doc['uid']}, {"$set": doc}, upsert=False)
        e = entries.find_one({'_id': doc['uid']})
        return str(e)
    def check_db(self, text):
        return check_DB(text)

def clean_and_save(uid):
    dirty = entries.find_one(uid)
    cleansed = dirty['parsed']
    try:
        cleansed['intent'] = cleansed['intent']['name']
    except:
        pass
    if cleansed['entities'] != []:
        leng = len(cleansed['entities'])
        for i in range(0,leng):
            try:
                item = cleansed['entities'][i]
                item.pop('extractor')
                item.pop('processors')
            except:
                pass
    runtime_training_data.insert_one(cleansed)


def check_DB(text):
    previous_entry = entries.find_one({'text': text})
    if previous_entry == None:
        return False
    else:
        self_confidence = previous_entry['parsed']['intent']['confidence']
        if self_confidence > threshold:
            return previous_entry
        else:
            return False
