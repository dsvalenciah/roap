
"""
Contains utility functions to works with learning-object and his metadata
fields schemas.
"""

import os
import json

from marshmallowjson.marshmallowjson import Definition


def LearningObjectMetadata(db_client):
    """Check if learning-object matches with a learning-object schema."""
    lom_schema = list(
        db_client.lom_schema.find().sort("created", -1).limit(1)
    )[0].get('lom')

    learning_object_metadata_schema = Definition(lom_schema).top()
    return learning_object_metadata_schema
