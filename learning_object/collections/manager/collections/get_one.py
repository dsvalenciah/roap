from ..exceptions import CollectionNotFoundError


def get_one(db_client, collection_id, user):
    _ = user.get('language')
    collection = db_client.locollection.find_one({
        '_id': collection_id
    })

    if not collection:
        raise CollectionNotFoundError(_('Collection not found'))

    sub_collections = list(db_client.sub_collection.find({
        'collection_id': collection_id
    }))

    collection.update({'sub_collections': sub_collections})
    return collection
