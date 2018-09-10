
"""
Contains utility functions to works with learning-object insert one.
"""

import json
from uuid import uuid4

from manager.exceptions.learning_object import LearningObjectFormatError

from manager.schemas.learning_object import LearningObject
from manager.schemas.learning_object_metadata import LearningObjectMetadata

from manager.utils.xml_to_dict import xml_to_dict

from bson.json_util import dumps

def get_last_learning_object_metadata_schema_id(db_client):
    return db_client.lom_schema.find().sort("created", -1)[0].get('_id')

def insert_one(
        db_client, learning_object_metadata, learning_object_category,
        learning_object_format, creator_id, learning_object_id=None,
        learning_object_file=None, ignore_schema=False, with_file=True):
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

    learning_object_metadata2 = learning_object_metadata.copy()

    if not ignore_schema:
        learning_object_metadata, errors = LearningObjectMetadata().dump(
            learning_object_metadata
        )
        if errors:
            pass
            # TODO: manage errors

    learning_object_metadata_schema_id = (
        get_last_learning_object_metadata_schema_id(db_client)
    )

    # TODO: validate learning object category.

    file_extension = ''
    if not learning_object_id:
        learning_object_id = str(uuid4())

    if with_file:
        if not learning_object_file:
            raise ValueError(
                'No have file'
            )
    else:
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