#Polymorphic Database functions

def find_one(databaseType, table, key_val):
	return databaseType.db_find_one(databaseType, table, key_val)

def insert_one(databaseType, table, doc):
	databaseType.db_insert_one(databaseType,table, doc)

def find(databaseType, table):
	return databaseType.db_find(databaseType, table)