
"""
Contains utility functions to works with learning-object insert one.
"""

import json

from manager.exceptions.learning_object import LearningObjectFormatError

from manager.schemas.learning_object import LearningObject
from manager.schemas.learning_object_metadata import LearningObjectMetadata

from manager.utils.xml_to_dict import xml_to_dict

from bson.json_util import dumps

def get_last_learning_object_metadata_schema_id(db_client):
    return db_client.lom_schema.find().sort("created", -1)[0].get('_id')

def insert_one(
        db_client, learning_object_metadata, learning_object_category,
        learning_object_format, learning_object_id, file_extension,
        creator_id, ignore_schema=False):
    """Insert learning object."""

    format_handler = {
        'xml': lambda lom: xml_to_dict(lom),
        'json': lambda lom: lom
    }

    if learning_object_format not in format_handler.keys():
        raise LearningObjectFormatError(['Unknown format.'])

    learning_object_metadata = (
        format_handler[learning_object_format](learning_object_metadata)
    )

    if not ignore_schema:
        learning_object_metadata = LearningObjectMetadata().dump(
            learning_object_metadata
        )

    learning_object_metadata_schema_id = (
        get_last_learning_object_metadata_schema_id(db_client)
    )

    # TODO: validate learning object category.

    if not file_extension:
        file_extension = (learning_object_metadata
            .get('technical', {})
            .get('format')
        )
        if isinstance(file_extension, list):
            file_extension = file_extension[0]
        if not file_extension:
            raise ValueError(
                f'{learning_object_id} no have extension'
            )

    learning_object_dict = dict(
        _id=learning_object_id,
        creator_id=creator_id,
        lom_schema_id=learning_object_metadata_schema_id,
        category=learning_object_category,
        metadata=learning_object_metadata,
        file_name=learning_object_id + '.' + file_extension,
    )

    learning_object, errors = LearningObject().dump(learning_object_dict)

    if errors:
        # TODO: report response errors.
        raise ValueError(errors)

    result = db_client.learning_objects.insert_one(
        learning_object
    )

    return result.inserted_id