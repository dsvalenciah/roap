
"""
Contains utility functions to works with learning-object get many.
"""

def get_many(db_client, filter_, range_, sorted_):
    """Get learning objects with query."""

    start, end = range_
    field, order = sorted_

    if filter_.get('q'):
        cursor = db_client.learning_objects.find(
            {'$text': {
                '$search': filter_.get('q'),
                '$diacriticSensitive': False,
                '$caseSensitive': False,
            }},
            {'rating': {'$meta': "textScore"}}
        )
        learning_objects = list(
            cursor
            .sort([('rating', {'$meta': "textScore"})])
            .skip(start)
            .limit(end - start)
        )
    else:
        cursor = db_client.learning_objects.find(filter_)
        learning_objects = list(
            cursor
            .sort([(field, -1 if order == 'DESC' else 1)])
            .skip(start)
            .limit(end - start)
        )

    return learning_objects, cursor.count()
