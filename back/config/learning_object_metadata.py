
"""
Contains utility functions to populate database with a default
learning-object-metadata-fields.
"""

import collections
import json
from uuid import uuid4
from datetime import datetime

from marshmallowjson.marshmallowjson import Definition

from bson.json_util import dumps


def learning_object_schema_populate(db):
    """Populate database with default learning-object-metadata-fields."""
    lom_schema = json.loads(dumps(
        db.lom_schema.find().sort("created", -1).limit(1)
    ))
    if not lom_schema:
        lom_schema = json.load(
            open('config/data/lom.json'),
            object_pairs_hook=collections.OrderedDict
        )
        Definition(lom_schema).top()
        db.lom_schema.insert_one(
            {
                '_id': uuid4().hex,
                'lom': lom_schema,
                'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
        )
