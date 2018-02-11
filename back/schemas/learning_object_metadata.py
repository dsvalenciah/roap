
"""
Contains utility functions to works with learning-object and his metadata
fields schemas.
"""

import os

from marshmallowjson.marshmallowjson import Definition

from pymongo import MongoClient


client = MongoClient(os.getenv('DB_HOST'), 27017)
db = client.roap


def is_valid_learning_object_metadata(learning_object_metadata):
    """Check if learning-object matches with a learning-object schema."""
    schema_fields = db.learning_object_metadata.find_one(
        {'_id': 'lom'}
    ).get('lom')

    learning_object_metadata_schema = Definition(schema_fields).top()
    if len(learning_object_metadata) > len(schema_fields):
        return {'attributes': 'invalid number'}
    else:
        return learning_object_metadata_schema.validate(
            learning_object_metadata
        )
