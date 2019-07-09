def get_many(db_client, filter_, range_, sorted_):
    start, end = range_
    query = filter_
    result = db_client.locollection.find_one(query, {'_id': 0,'sub_collections': 1})
    if result:
        sub_collections = result.get('sub_collections')[start: end-start +1]
        for sub_collection in sub_collections:
            sub_collection.update({'lo_quantity': db_client.learning_objects.find({'sub_collection_id': sub_collection.get('id_')}).count()})
        return sub_collections, len(result.get('sub_collections'))
    else:
        return [], 0