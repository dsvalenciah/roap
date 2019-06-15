from ..schemas import Collection

def modify_one(db_client, collection_id, new_collection):
    old_collection = db_client.collections.find_one({
        '_id': collection_id
    })
    new_collection, errors = Collection(
        exclude=['_id']
    ).dump(new_collection)

    if errors:
        print("ERRORR")
        print("MODIFY COLLECTION")
    
    db_client.collections.update_one(
        {'_id': old_collection.get('_id')},
        {'$set': new_collection}
    )