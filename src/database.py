# Imports MongoClient for base level access to the local MongoDB
from pymongo import MongoClient


class Database:
    # Class static variables used for database host ip and port information, database name
    # Static variables are referred to by using <class_name>.<variable_name>
    HOST = '127.0.0.1'
    PORT = '27017'
    DB_NAME = 'weather_db'

    def __init__(self):
        self._db_conn = MongoClient(f'mongodb://{Database.HOST}:{Database.PORT}')
        self._db = self._db_conn[Database.DB_NAME]
    
    # This method finds a single document using field information provided in the key parameter
    # It assumes that the key returns a unique document. It returns None if no document is found
    def get_single_data(self, collection, key):
        try:
            db_collection = self._db[collection]
            document = db_collection.find_one(key)
            return document
        except Exception as e:
            print("An exception occurred ::", e)
            return False
    
    # This method inserts the data in a new document. It assumes that any uniqueness check is done by the caller
    def insert_single_data(self, collection, data):
        try:
            db_collection = self._db[collection]
            document = db_collection.insert_one(data)
            return document.inserted_id
        except Exception as e:
            print("An exception occurred ::", e)
            return False

    # This method updates the data in an existing document. It assumes that any uniqueness check is done by the caller
    def update_single_data(self, collection, filter, data):
        try:
            db_collection = self._db[collection]
            document = db_collection.update_one(filter, {'$set': data})
            return document
        except Exception as e:
            print("An exception occurred ::", e)
            return False

    # This method creates new collection
    def create_coll(self, collection):
        try:
            col_name = collection
            if col_name in self._db.list_collection_names():
                db_collection = self._db[collection]
                db_collection.drop()
                print("Dropped existing collection!")
            else:
                print("Collection did not exist, created now!")
            new_coll = self._db.create_collection(collection)
            return new_coll
        except Exception as e:
            print("An exception occurred ::", e)
            return False

    def find_many_data(self, collection, key):
        try:
            db_collection = self._db[collection]
            result = db_collection.find(key)
            print("Query successful")
            return result
        except Exception as e:
            print("An exception occurred ::", e)
            return False

    def insert_many_data(self, collection, data):
        try:
            db_collection = self._db[collection]
            document = db_collection.insert_many(data)
            return collection
        except Exception as e:
            print("An exception occurred ::", e)
            return False

    def aggregate_data(self, collection, query):
        try:
            db_collection = self._db[collection]
            agg_result = db_collection.aggregate(query)
            return agg_result
        except Exception as e:
            print("An exception occurred ::", e)
            return False