
"""
Contains utility functions to populate database with a default
learning-object-metadata-fields.
"""

import json
import os
from uuid import uuid4

from bson.json_util import dumps

from pymongo import MongoClient


client = MongoClient(os.getenv('DB_HOST'), 27017)
db = client.roap


def learning_object_schema_populate():
    """Populate database with default learning-object-metadata-fields."""
    schema_fields = json.loads(dumps(db.learning_object_metadata.find()))
    if not schema_fields:
        schema_fields = json.load(
            open('config/default_learning_object_fields_schema.json')
        )
        for schema_field in schema_fields:
            schema_field.update({'_id': uuid4().hex})
            db.learning_object_metadata.insert_one(schema_field)
