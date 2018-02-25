
"""
Contains utility functions to populate database with a default
collections categories.
"""

import collections
import json

from bson.json_util import dumps


def collections_category_populate(db):
    """Populate database with default collections categories."""
    collections_category_schema = json.loads(dumps(
        db.collections_category.find({'_id': 'collections_category'})
    ))

    if not collections_category_schema:
        collections_category_schema = json.load(
            open('config/data/collections_category.json'),
            object_pairs_hook=collections.OrderedDict
        )
        db.collections_category.insert_one(
            {
                '_id': 'collections_category',
                'collections_category': collections_category_schema
            }
        )
