from ..schemas import LOCollection
from ..exceptions import CollectionSchemaError, UserPermissionError
from uuid import uuid4


def insert_one(db_client, collection_dict, user):
    _ = user.get('language')

    if user.get('role') != 'administrator':
        raise UserPermissionError(_('User can\'t create Collections'))

    collection_id = str(uuid4())
    for sub_collection in collection_dict.get('sub_collections'):
        sub_collection.update({'id_': str(uuid4()), 'los_quantity': 0})
    
    collection_dict.update({'_id': collection_id})
    collection, errors = LOCollection().dump(collection_dict)

    if errors:
        raise CollectionSchemaError(errors)
    
    result = db_client.locollection.insert_one(collection)

    return result.inserted_id