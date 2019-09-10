
"""
Contains utility functions to works with learning-object insert one.
"""

from manager.utils.i18n_error import ErrorTranslator
from manager.utils.file_manager import StorageUnit
from manager.utils.dict_to_xml import dict_to_xml as dict_with_xml
from manager.utils.xml_to_dict import xml_to_dict as xml_with_dict
from manager.schemas.learning_object_metadata import LearningObjectMetadata
from manager.schemas.learning_object import LearningObject
from datetime import datetime
import re
from manager.exceptions.learning_object import (
    LearningObjectFormatError, LearningObjectMetadataSchemaError,
    LearningObjectSchemaError, LearningObjectFile
)
import json
import mimetypes
from uuid import uuid4

mimetypes.init()


def get_last_learning_object_metadata_schema_id(db_client):
    return db_client.lom_schema.find().sort("created", -1)[0].get('_id')


def insert_one(
        db_client, learning_object_metadata, learning_object_format,
        creator_id, user_language, learning_object_collection_id='', learning_object_sub_collection_id='', learning_object_id=None,
        learning_object_file=None, ignore_schema=False, with_file=True, status='pending'):
    """Insert learning object."""
    _ = user_language
    format_handler = {
        'xml': lambda lom: xml_with_dict(lom),
        'json': lambda lom: dict_with_xml(lom)
    }

    if learning_object_format not in format_handler.keys():
        raise LearningObjectFormatError(_('Unknown format.'))

    (
        learning_object_metadata_dict,
        learning_object_metadata_xml
    ) = (
        format_handler[learning_object_format](learning_object_metadata)
    )

    if not ignore_schema:
        errors = LearningObjectMetadata(
            db_client
        ).validate(learning_object_metadata_dict)
        if errors:
            errors_translator = ErrorTranslator(_)
            raise LearningObjectMetadataSchemaError(
                errors_translator.i18n_error(errors))

    learning_object_metadata_schema_id = (
        get_last_learning_object_metadata_schema_id(db_client)
    )

    # TODO: validate learning object category.

    if not learning_object_id:
        learning_object_id = str(uuid4())

    if with_file:
        if not learning_object_file:
            raise LearningObjectFile(_('File not found.'))
        file_extension = '.' + \
            learning_object_file.get('name', '.').split('.')[-1]
        file_metadata = {
            '_id': learning_object_id,
            'extension': file_extension,
            'name': learning_object_file.get('name'),
            'mime_type': learning_object_file.get('mimeType'),
            'size': learning_object_file.get('size'),
            'last_modified': learning_object_file.get('lastModified')
        }
        storage_unit = StorageUnit(exceptions_language_handler=user_language)
        storage_unit.store(
            learning_object_file.get('base64File'),
            file_metadata
        )
    else:
        file_extension = (learning_object_metadata_dict
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
        file_name = learning_object_id + file_extension
        mime_type, _ = mimetypes.guess_type(file_name)
        file_metadata = {
            '_id': learning_object_id,
            'extension': file_extension,
            'name': file_name,
            'mime_type': mime_type,
            'size': None,
            'last_modified': None
        }
    if(file_extension == '.zip'):
        learning_object_metadata_dict['technical']['location'] = (
            f'/learning-object-file-renderer/{learning_object_id}/'
        )
    else:
        learning_object_metadata_dict['technical']['location'] = (
            f'/learning-object-file-renderer/{learning_object_id}{file_extension}'
        )

    learning_object_dict = dict(
        _id=learning_object_id,
        creator_id=creator_id,
        lom_schema_id=learning_object_metadata_schema_id,
        metadata=learning_object_metadata_dict,
        metadata_xml=learning_object_metadata_xml,
        file_metadata=file_metadata,
        status=status
    )

    if learning_object_collection_id != '':
        learning_object_dict.update({'collection_id': learning_object_collection_id,
                                     'sub_collection_id': learning_object_sub_collection_id})

    learning_object, errors = LearningObject().dump(learning_object_dict)

    if errors:
        raise LearningObjectSchemaError(errors)

    result = db_client.learning_objects.insert_one(learning_object)

    return result.inserted_id
