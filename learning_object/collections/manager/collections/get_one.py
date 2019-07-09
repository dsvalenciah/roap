from ..exceptions import CollectionNotFoundError


def get_one(db_client, collection_id, user):
    _ = user.get('language')
    collection = db_client.locollection.find_one({
        '_id': collection_id
    })

    if not collection:
        raise CollectionNotFoundError(_('Collection not found'))

    lo_quantity = db_client.learning_objects.find({ 'collection_id': collection_id }).count()

    collection.update({'lo_quantity': lo_quantity})

    for sub_collection in collection.get('sub_collections'):
            sub_collection.update({'lo_quantity': db_client.learning_objects.find({'sub_collection_id': sub_collection.get('id_')}).count()})
    return collection
