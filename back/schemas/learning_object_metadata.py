
"""
Contains utility functions to works with learning-object and his metadata
fields schemas.
"""

import os
import json

from marshmallowjson.marshmallowjson import Definition

from pymongo import MongoClient
from bson.json_util import dumps


client = MongoClient(os.getenv('DB_HOST'), 27017)
db = client.roap


def is_valid_learning_object_metadata(lom):
    """Check if learning-object matches with a learning-object schema."""
    lom_schema = json.loads(dumps(
        db.lom_schema.find().sort("created", -1).limit(1)
    ))[0].get('lom')

    learning_object_metadata_schema = Definition(lom_schema).top()
    if len(lom) > len(lom_schema):
        return {'attributes': 'invalid number'}
    else:
        return learning_object_metadata_schema.validate(
            lom
        )
