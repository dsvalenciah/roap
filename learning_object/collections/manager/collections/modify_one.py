from ..schemas import LOCollection
from ..exceptions import (
    UserPermissionError, CollectionNotFoundError, CollectionSchemaError, SubCollectionUndeleteError)
from uuid import uuid4


def modify_one(db_client, collection_id, new_collection, user):
    _ = user.get('language')

    if user.get('role') != 'administrator':
        raise UserPermissionError(_('User can\'t modify Collections'))

    old_collection = db_client.locollection.find_one({
        '_id': collection_id
    })

    if not old_collection:
        raise CollectionNotFoundError(_('Collection not found'))

    for old_sub_collection in old_collection.get('sub_collections'):
        esta = False
        for sub_collection in new_collection.get('sub_collections'):
            if (sub_collection.get('id_') == old_sub_collection.get('id_')):
                esta = True

        if not esta:
            if (db_client.learning_objects.find({'sub_collection_id': old_sub_collection.get('id_')}).count() > 0):
                raise SubCollectionUndeleteError(
                    _('No puede eliminar subcolecciones que contengan objetos.'))

    for new_sub_collection in new_collection.get('sub_collections'):
        if not 'id_' in new_sub_collection:
            new_sub_collection.update({'id_': str(uuid4())})

    new_collection, errors = LOCollection(
        exclude=['_id']
    ).dump(new_collection)

    if errors:
        raise CollectionSchemaError(errors)

    db_client.locollection.update_one(
        {'_id': old_collection.get('_id')},
        {'$set': new_collection}
    )
