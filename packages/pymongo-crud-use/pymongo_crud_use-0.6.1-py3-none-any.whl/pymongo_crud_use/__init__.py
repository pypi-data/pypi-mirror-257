# Import necessary functions or classes to be accessible when the package is imported
from .mongo_functions import (
    uuid_id,
    initialize_collection,
    initialize_collection_with_certificate,
    test_connection,
    set_data,
    get_data,
    get_all_data,
    get_data_one,
    remove_data_bool,
    remove_data,
    update_data,
    delete_db,
    count_db_bool,
    count_all_db,
    search_data_by_field,
    upsert_data,
    search_across_fields,
    search_all_fields,
    close_connection
)

# Define __all__ to specify what symbols will be exported when using "from pymongo_crud_use import *"
__all__ = [
    'uuid_id',
    'initialize_collection',
    'initialize_collection_with_certificate',
    'test_connection',
    'set_data',
    'get_data',
    'get_all_data',
    'get_data_one',
    'remove_data_bool',
    'remove_data',
    'update_data',
    'delete_db',
    'count_db_bool',
    'count_all_db',
    'search_data_by_field',
    'upsert_data',
    'search_across_fields',
    'search_all_fields',
    'close_connection'
]
