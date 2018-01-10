from uuid import uuid4
import json
import os

from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient(os.getenv('DB_HOST'), 27017)
db = client.roap


def learning_object_schema_populate():
    schema_fields = json.loads(dumps(db.metadata.find()))
    if not schema_fields:
        schema_fields = json.load(
            open("config/default_learning_object_fields_schema.json")
        )
        for schema_field in schema_fields:
            schema_field.update({"_id": uuid4().hex})
            db.metadata.insert_one(schema_field)