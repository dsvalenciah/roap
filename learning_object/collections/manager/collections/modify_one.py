from ..schemas import Collection
from ..exceptions import (
    UserPermissionError, CollectionNotFoundError, CollectionSchemaError)


def modify_one(db_client, collection_id, new_collection, user):
    _ = user.get('language')

    if user.get('role') != 'administrator':
        raise UserPermissionError(_('User can\'t modify Collections'))

    old_collection = db_client.collections.find_one({
        '_id': collection_id
    })

    if not old_collection:
        raise CollectionNotFoundError(_('Collection not found'))

    new_collection, errors = Collection(
        exclude=['_id']
    ).dump(new_collection)

    if errors:
        raise CollectionSchemaError(errors)

    db_client.collections.update_one(
        {'_id': old_collection.get('_id')},
        {'$set': new_collection}
    )
