def get_many(db_client, filter_, range_, sorted_):
    start, end = range_
    field, order = sorted_

    if filter_.get('q'):
        query = {'$text': {
            '$search': filter_.get('q'),
            '$diacriticSensitive': False,
            '$caseSensitive': False,
        }}
        cursor = db_client.sub_collection.find(
            query
        )
        sub_collections = list(
            cursor
            .skip(start)
            .limit((end - start) + 1)
        )
    else:
        query = filter_
        cursor = db_client.sub_collection.find(query)
        sub_collections = list(
            cursor
            .sort([(field, -1 if order == 'DESC' else 1)])
            .skip(start)
            .limit((end - start) + 1)
        )

    return sub_collections, cursor.count()
