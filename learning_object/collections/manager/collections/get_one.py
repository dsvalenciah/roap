def get_one(db_client, collection_id):
    collection = db_client.collections.find_one({
        '_id': collection_id
    })

    return collection