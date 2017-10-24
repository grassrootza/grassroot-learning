#Polymorphic Database functions

def find_one(databaseType, table, key_val):
	return databaseType.db_find_one(databaseType, table, key_val)

def insert_one(databaseType, doc):
	databaseType.db_insert_one(databaseType, doc)

def find(databaseType, table):
	return databaseType.db_find(databaseType, table)

def load_old_text(databaseType, uid):
	return databaseType.load_old_Text(databaseType, uid)

def find_previous_entry(databaseType, uid):
	return databaseType.find_previous_Entry(databaseType, uid)

def find_clean_and_save(databaseType, uid):
    databaseType.find_clean_save(databaseType, uid)

def update_db(databaseType, doc):
    databaseType.update_DB(databaseType, doc)

def check_database(databaseType, text):
    return databaseType.check_db(databaseType, text)