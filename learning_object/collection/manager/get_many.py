
"""
Contains utility functions to works with learning-object get many.
"""

def get_many(db_client, offset, count, search=None):
    """Get learning objects with query."""

    if search:
        learning_objects = list(
            db_client.learning_objects.find(
                {'$text': {
                    '$search': search,
                    '$diacriticSensitive': False,
                    '$caseSensitive': False,
                }},
                {'rating': {'$meta': "textScore"}}
            ).sort(
                [('rating', {'$meta': "textScore"})]
            ).skip(offset).limit(count)
        )

        return learning_objects

    learning_objects = list(
        db_client.learning_objects.find()
            .sort([('created', -1)])
            .skip(offset)
            .limit(count)
    )

    return learning_objects