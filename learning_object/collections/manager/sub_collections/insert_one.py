from ..schemas import SubCollection
from ..exceptions import CollectionNotFoundError, UserPermissionError, SubCollectionSchemaError
from uuid import uuid4


def insert_one(db_client, collection_id, name_sub_collection, user):
    _ = user.get('language')

    if user.get('role') != 'administrator':
        raise UserPermissionError(
            _('User can\'t modify sub collections of collections'))

    collection = db_client.locollection.find({
        '_id': collection_id
    })

    if not collection:
        raise CollectionNotFoundError(_('Collection not found'))

    sub_collection_id = str(uuid4())
    sub_collection_dict = dict(
        _id=sub_collection_id,
        name=name_sub_collection,
        collection_id=collection_id
    )

    sub_collection, errors = SubCollection().dump(sub_collection_dict)

    if errors:
        raise SubCollectionSchemaError(errors)

    result = db_client.sub_collection.insert_one(sub_collection)

    return result.inserted_id
