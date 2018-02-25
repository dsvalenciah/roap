
"""
Contains utility functions to populate database with a default
learning-object-metadata-fields.
"""

import collections
import json

from marshmallowjson.marshmallowjson import Definition

from bson.json_util import dumps


def learning_object_schema_populate(db):
    """Populate database with default learning-object-metadata-fields."""
    lom_schema = json.loads(dumps(
        db.learning_object_metadata.find({'_id': 'lom'})
    ))
    if not lom_schema:
        lom_schema = json.load(
            open('config/data/lom.json'),
            object_pairs_hook=collections.OrderedDict
        )
        Definition(lom_schema).top()
        db.learning_object_metadata.insert_one(
            {'_id': 'lom', 'lom': lom_schema}
        )
