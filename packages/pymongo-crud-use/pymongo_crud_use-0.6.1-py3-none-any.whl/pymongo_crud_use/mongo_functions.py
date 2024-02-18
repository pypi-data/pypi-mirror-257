"""
This module provides functions for interacting with a MongoDB database using pymongo.
"""

from typing import Any, Dict, List, Optional, Union
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult
from uuid_extensions import uuid7str

def uuid_id() -> str:
    """
    Generate a UUID using the UUID7 strategy.

    Returns:
    - str: A string representation of the generated UUID.
    """
    return uuid7str()

def initialize_collection(uri: str, db_name: str, collection_name: str) -> Collection:
    """
    Initialize and return the MongoDB collection.
    """
    try:
        client = MongoClient(uri)
        return client[db_name][collection_name]
    except Exception as e:
        raise ValueError(f"Error initializing collection: {str(e)}")

def initialize_collection_with_certificate(uri: str, certificate_path: str, db_name: str, collection_name: str) -> Collection:
    """
    Initialize and return the MongoDB collection using TLS certificate authentication.

    Parameters:
    - uri: MongoDB URI string.
    - certificate_path: Path to the TLS certificate file.
    - db_name: Name of the MongoDB database.
    - collection_name: Name of the collection within the database.

    Returns:
    - MongoDB collection object.
    """
    try:
        # Initialize MongoClient with TLS certificate authentication
        client = MongoClient(uri,
                             tls=True,
                             tlsCertificateKeyFile=certificate_path,
                             server_api=ServerApi('1'))

        # Access the specified database and collection
        return client[db_name][collection_name]

    except Exception as e:
        raise ValueError(f"Error initializing collection with certificate: {str(e)}")

def test_connection(collection: Collection) -> bool:
    """
    MongoDB connection testing
    """
    try:
        # The ismaster command is cheap and does not require auth.
        collection.database.client.admin.command('ismaster')
        return True
    except Exception as e:
        print(f"An error occurred while trying to connect: {str(e)}")
        return False

def set_data(collection: Collection, data: Dict[str, Any]) -> InsertOneResult:
    """
    Insert data into the MongoDB collection.
    """
    try:
        return collection.insert_one(data)
    except Exception as e:
        raise ValueError(f"Error setting data: {str(e)}")


def get_data(collection: Collection) -> List[Dict[str, Any]]:
    """
    Retrieve data from the MongoDB collection where 'available' is True.
    """
    try:
        cursor = collection.find({'available': True})
        data_list = [doc for doc in cursor]
        return data_list
    except Exception as e:
        raise ValueError(f"Error getting data: {str(e)}")

def get_all_data(collection: Collection) -> List[Dict[str, Any]]:
    """
    Retrieve all data from the MongoDB collection.
    """
    try:
        cursor = collection.find()
        data_list = [doc for doc in cursor]
        return data_list
    except Exception as e:
        raise ValueError(f"Error getting all data: {str(e)}")

def get_data_one(collection: Collection, id_data: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single document from the MongoDB collection by its ID.
    """
    try:
        document = collection.find_one({'_id': id_data})
        if document is not None:
            return document
        else:
            return None
    except Exception as e:
        raise ValueError(f"Error getting data by ID: {str(e)}")

def remove_data_bool(collection: Collection, id_data: str) -> UpdateResult:
    """
    Remove data from the MongoDB collection by its ID and set 'available' to False.
    """
    try:
        return collection.update_one({'_id': id_data}, {'$set': {'available': False}})
    except Exception as e:
        raise ValueError(f"Error removing data (bool): {str(e)}")

def remove_data(collection: Collection, id_data: str) -> DeleteResult:
    """
    Remove data from the MongoDB collection by its ID.
    """
    try:
        return collection.delete_one({'_id': id_data})
    except Exception as e:
        raise ValueError(f"Error removing data: {str(e)}")

def update_data(collection: Collection, id_data: str, data: Dict[str, Any]) -> UpdateResult:
    """
    Update data in the MongoDB collection by its ID.
    """
    try:
        return collection.update_one({'_id': id_data}, {'$set': data})
    except Exception as e:
        raise ValueError(f"Error updating data: {str(e)}")

def delete_db(collection: Collection) -> DeleteResult:
    """
    Delete all data from the MongoDB collection.
    """
    try:
        return collection.delete_many({})
    except Exception as e:
        raise ValueError(f"Error deleting database: {str(e)}")

def count_db_bool(collection: Collection) -> int:
    """
    Count documents in the MongoDB collection where 'available' is True.
    """
    try:
        return collection.count_documents({'available': True})
    except Exception as e:
        raise ValueError(f"Error counting documents (bool): {str(e)}")

def count_all_db(collection: Collection) -> int:
    """
    Count all documents in the MongoDB collection.
    """
    try:
        return collection.count_documents({})
    except Exception as e:
        raise ValueError(f"Error counting all documents: {str(e)}")

def search_data_by_field(collection: Collection, field_name: str, field_value: Any) -> Union[List[Dict[str, Any]], None]:
    """
    Retrieve data from the MongoDB collection based on a specific field and its value.
    """
    try:
        cursor = collection.find({field_name: field_value})
        documents = [doc for doc in cursor]
        return documents if documents else None
    except Exception as e:
        raise ValueError(f"Error searching data by field: {str(e)}")

def upsert_data(collection: Collection, query: Dict[str, Any], data: Dict[str, Any]) -> UpdateResult:
    """
    Update existing data if found, or insert new data if not found.
    """
    try:
        return collection.update_one(query, {'$set': data}, upsert=True)
    except Exception as e:
        raise ValueError(f"Error upserting data: {str(e)}")

def search_across_fields(collection: Collection, search_query: str) -> Union[List[Dict[str, Any]], None]:
    """
    Search across all fields of the MongoDB collection and return matching documents.
    """
    try:
        sample_document = collection.find_one()

        if sample_document is not None:
            query = {
                "$or": [{field: {"$regex": search_query, "$options": "i"}} for field in sample_document.keys()]
            }

            cursor = collection.find(query)
            documents = [doc for doc in cursor]
            return documents if documents else None
        else:
            return None
    except Exception as e:
        raise ValueError(f"Error searching across fields: {str(e)}")

def search_all_fields(collection: Collection, search_term: str) -> Union[List[Dict[str, Any]], None]:
    """
    Search for the given term in all fields of the MongoDB collection.
    """
    try:
        sample_document = collection.find_one()

        if sample_document is not None:
            query = {
                "$or": [{key: {"$regex": search_term.lower(), "$options": "i"}} for key in sample_document.keys()]
            }

            cursor = collection.find(query)
            documents = [doc for doc in cursor]
            return documents if documents else None
        else:
            return None
    except Exception as e:
        raise ValueError(f"Error searching all fields: {str(e)}")

def close_connection(collection: Collection):
    """
    Close the connection to the MongoDB database.
    """
    try:
        return collection.client.close()
    except Exception as e:
        raise ValueError(f"Error closing connection: {str(e)}")
