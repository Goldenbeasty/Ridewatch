from pymongo import MongoClient
import time

# Establish a connection to the MongoDB server
client = MongoClient('mongodb://mongodb:27017')

# Access a database and collection
db = client['mydatabase']
collection = db['registration_times']

def check_and_store_registration_time(registration_time: dict) -> bool:
    # returns True if new time
    # Check if a document with the same "time" and "instructor" already exists
    query = {
        'time': registration_time['time'],
        'instructor': registration_time['instructor']
    }

    existing_document = collection.find_one(query)

    if existing_document:
        # Entry already exists
        if existing_document.get('is_taken') is True: # case: someone has given up their time
            # Set the 'is_taken' flag to False
            collection.update_one(query, {'$set': {'is_taken': False}})
            return True
        else:
            return False

    registration_time['time_first_seen'] = int(time.time())
    # Entry doesn't exist, insert it into the database
    collection.insert_one(registration_time)
    return True

def update_is_taken_flag(registration_times: list) -> None:
    # Get a list of existing documents from the database
    existing_documents = collection.find(
        {'$or': [
            {'is_taken': {'$exists': False}},
            {'is_taken': {'$ne': True}}
        ]},
        {'time': 1, 'instructor': 1, 'is_taken': 1}
    )

    # Create a set of unique identifiers for the input registration times
    input_identifiers = {(doc['time'], doc['instructor']) for doc in registration_times}

    # Update the 'is_taken' flag for existing documents not present in the input list
    for existing_doc in existing_documents:
        identifier = (existing_doc['time'], existing_doc['instructor'])
        if identifier not in input_identifiers:
            collection.update_one(
                {'time': existing_doc['time'], 'instructor': existing_doc['instructor']},
                {'$set': {'is_taken': True}}
            )
