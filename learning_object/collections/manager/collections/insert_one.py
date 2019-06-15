from ..schemas import LOCollection
from ..exceptions import CollectionSchemaError, UserPermissionError
from uuid import uuid4


def insert_one(db_client, collection_name, user):
    _ = user.get('language')

    if user.get('role') != 'administrator':
        raise UserPermissionError(_('User can\'t create Collections'))

    collection_id = str(uuid4())
    collection_dict = dict(
        _id=collection_id,
        name=collection_name
    )

    collection, errors = LOCollection().dump(collection_dict)

    if errors:
        raise CollectionSchemaError(errors)
    
    result = db_client.locollection.insert_one(collection)

    return result.inserted_id