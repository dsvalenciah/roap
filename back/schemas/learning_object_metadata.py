
"""
Contains utility functions to works with learning-object and his metadata
fields schemas.
"""

import json
import os

from bson.json_util import dumps

from marshmallowjson.marshmallowjson import Definition

from pymongo import MongoClient


client = MongoClient(os.getenv('DB_HOST'), 27017)
db = client.roap


def is_valid_learning_object(learning_object):
    """Check if learning-object matches with a learning-object schema."""
    schema_fields = json.loads(dumps(db.learning_object_metadata.find_one(
        {'_id': 'lom'}
    )))

    learning_object_schema = Definition(schema_fields).top()
    if len(learning_object) > len(schema_fields):
        return {'attributes': 'invalid number'}
    else:
        return learning_object_schema.validate(learning_object)
