
"""
Contains utility functions to works with learning-objects.
"""


from datetime import datetime
from uuid import uuid4

from exceptions.learning_object import (
    LearningObjectNotFoundError, LearningObjectSchemaError,
    LearningObjectUnmodifyError, LearningObjectUndeleteError,
    LearningObjectFormatError, LearningObjectMetadataSchemaError
)

from schemas.learning_object_metadata import is_valid_learning_object_metadata
from schemas.learning_object import is_valid_learning_object

from utils.dict_to_xml import dict_to_xml
from utils.regex import only_letters

from marshmallowjson.marshmallowjson import Definition


def new_learning_object(name, db, learning_object_metadata, user):
    """Create a learning object dict."""
    # TODO: add salt to file configuration
    learning_object = {
        '_id': uuid4().hex,
        'user_id': user.get('_id'),
        'created': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'modified': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'schema': db.learning_object_metadata.find_one(
            {'_id': 'lom'}
        ).get('lom'),
        'metadata': learning_object_metadata,
        'state': "unevaluated",
        'user_ranking': 0,
        'evaluator_ranking': 0,
        'files': [],
    }
    return learning_object


class LearningObject():
    """docstring for Learning Object."""

    def __init__(self, db):
        """Init."""
        self.db = db

    def insert_one(self, learning_object_metadata, user_id):
        """Insert learning object."""
        if learning_object_metadata and user_id:
            errors = is_valid_learning_object_metadata(
                learning_object_metadata
            )
            if errors:
                raise LearningObjectMetadataSchemaError(errors)

            user = db.users.find_one({"_id": user_id})
            if not user:
                raise LearningObjectUserIdNotFound({
                    'errors': ['User uid not found.']
                })

            # TODO: add files-path manager
            learning_object = new_learning_object(
                self.db, learning_object_metadata, user_id
            )
            errors = is_valid_learning_object(learning_object)
            if errors:
                raise LearningObjectSchemaError(errors)

            result = db.learning_objects.insert_one(
                learning_object
            )
            return result.inserted_id

    def get_one(self, uid, format_):
        """Get a learning object by uid."""
        # TODO: returns metadata or all object content?
        learning_object = self.db.learning_objects.find_one({'_id': uid})
        if not learning_object:
            raise LearningObjectNotFoundError(
                ['Learning Object uid not found.']
            )
        if format_ == 'xml':
            return dict_to_xml(learning_object.get('metadata'))
        elif format_ == 'json':
            return learning_object.get('metadata')
        else:
            raise LearningObjectFormatError(
                ['Format not found.']
            )

    def get_many(self, query):
        """Get learning objects with query."""
        if query and query.get('offset') and query.get('count'):
            try:
                offset = int(query.get('offset'))
                count = int(query.get('count'))
            except ValueError as e:
                raise ValueError(['Invalid offset or count parameters.'])
            enabled_fields = [
                # TODO: fix it and remove find().
            ]
            correct_fields = [
                only_letters(x) for x in query.keys()
                if x in enabled_fields
            ]
            if False not in correct_fields:
                fields_to_use = [
                    {x: {'$regex': f'.*{query.get(x)}.*'}}
                    for x in query.keys()
                    if x in enabled_fields
                ]
                query = {'$and': fields_to_use} if fields_to_use else {}
                learning_objects = self.db.learning_object.find(query)
                return learning_objects.skip(offset).limit(count)
            else:
                raise ValueError(['Invalid parameters value.'])
        else:
            return self.db.learning_object.find()

    def modify_one(self, uid, learning_object):
        """Modify learning object."""
        old_learning_object = self.db.learning_objects.find_one({'_id': uid})
        if not old_learning_object:
            raise LearningObjectNotFoundError({
                'errors': ['Learning Object uid not found.']
            })

        learning_object_schema = Definition(
            old_learning_object.get('schema')
        ).top()

        errors = learning_object_schema.validate(learning_object)

        if errors:
            raise LearningObjectMetadataSchemaError(errors)

        result = self.db.learning_objects.update_one(
            {'_id': uid},
            {'$set': {
                'metadata': learning_object,
                'modified': str(
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ),
            }}
        )
        if not result.modified_count:
            raise LearningObjectUnmodifyError(
                ['The Learning Object is not modified.']
            )

    def delete_one(self, uid):
        """Delete a learning object by uid."""
        learning_object = self.db.learning_objects.find_one({'_id': uid})
        if not learning_object:
            raise LearningObjectNotFoundError({
                'errors': ['Learning Object uid not found.']
            })
        result = self.db.learning_objects.delete_one({'_id': uid})
        if not result.deleted_count:
            raise LearningObjectUndeleteError(
                ['Learning Object is not deleted.']
            )
