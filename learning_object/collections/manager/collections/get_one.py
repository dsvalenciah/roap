from ..exceptions import CollectionNotFoundError


def get_one(db_client, collection_id, user):
    collection = db_client.collections.find_one({
        '_id': collection_id
    })

    _ = user.get('language')
    if not collection:
        raise CollectionNotFoundError(_('Collection not found'))
    
    return collection
