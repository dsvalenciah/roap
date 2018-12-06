
"""
Contains utility functions to works with learning-object insert one.
"""

import json
import mimetypes
from uuid import uuid4

mimetypes.init()

from manager.exceptions.learning_object import (
    LearningObjectFormatError, LearningObjectMetadataSchemaError,
    LearningObjectSchemaError, LearningObjectFileNotFound
)

import re

from datetime import datetime

from manager.schemas.learning_object import LearningObject
from manager.schemas.learning_object_metadata import LearningObjectMetadata

from manager.utils.xml_to_dict import xml_to_dict
from manager.utils.file_manager import StorageUnit


def get_last_learning_object_metadata_schema_id(db_client):
    return db_client.lom_schema.find().sort("created", -1)[0].get('_id')


def insert_one(
        db_client, learning_object_metadata, learning_object_format,
        creator_id, user_language, learning_object_category='', learning_object_id=None,
        learning_object_file=None, ignore_schema=False, with_file=True):
    """Insert learning object."""
    _ = user_language
    format_handler = {
        'xml': lambda lom: xml_to_dict(lom),
        'json': lambda lom: lom
    }

    if learning_object_format not in format_handler.keys():
        raise LearningObjectFormatError(_('Unknown format.'))

    learning_object_metadata = (
        format_handler[learning_object_format](learning_object_metadata)
    )

    if not ignore_schema:
        errors = LearningObjectMetadata(
            db_client
        ).validate(learning_object_metadata)
        if errors:
            raise LearningObjectMetadataSchemaError(errors)

    learning_object_metadata_schema_id = (
        get_last_learning_object_metadata_schema_id(db_client)
    )

    # TODO: validate learning object category.

    if not learning_object_id:
        learning_object_id = str(uuid4())

    if with_file:
        if not learning_object_file:
            raise LearningObjectFileNotFound(_('File not found.'))
        file_metadata = {
            '_id': learning_object_id,
            'extension': mimetypes.guess_extension(
                learning_object_file.get('mimeType')
            ),
            'name': learning_object_file.get('name'),
            'mime_type': learning_object_file.get('mimeType'),
            'size': learning_object_file.get('size'),
            'last_modified': learning_object_file.get('lastModified')
        }
        storage_unit = StorageUnit()
        storage_unit.store(
            learning_object_file.get('base64File'),
            file_metadata
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
                _('{learning_object_id} no have extension.').format(
                    learning_object_id=learning_object_id)
            )
        file_extension = '.' + file_extension
        file_metadata = {
            '_id': learning_object_id,
            'extension': file_extension,
            'name': learning_object_id + file_extension,
            'mime_type': None,
            'size': None,
            'last_modified': None
        }

    learning_object_metadata['technical']['location'] = (
        f'/learning-object-collection/{learning_object_id}/show'
    )

    learning_object_dict = dict(
        _id=learning_object_id,
        creator_id=creator_id,
        lom_schema_id=learning_object_metadata_schema_id,
        category=learning_object_category,
        metadata=learning_object_metadata,
        file_metadata=file_metadata
    )

    learning_object, errors = LearningObject().dump(learning_object_dict)

    if errors:
        raise LearningObjectSchemaError(errors)

    result = db_client.learning_objects.insert_one(learning_object)

    return result.inserted_id
