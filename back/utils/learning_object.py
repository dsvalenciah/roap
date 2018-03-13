
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

from exceptions.user import (
    UserInactiveError, UserPermissionError
)

from schemas.learning_object_metadata import is_valid_learning_object_metadata
from schemas.learning_object import is_valid_learning_object

from utils.dict_to_xml import dict_to_xml
from utils.regex import only_letters

from marshmallowjson.marshmallowjson import Definition


def new_learning_object(db, learning_object_metadata, user_id):
    """Create a learning object dict."""
    # TODO: add salt to file configuration
    learning_object = {
        '_id': uuid4().hex,
        'user_id': user_id,
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

    def insert_one(self, learning_object_metadata, user, ignore_schema=False):
        """Insert learning object."""
        user_deleted = user.get('deleted')
        user_role = user.get('role')
        if user_deleted or user_role == 'unknown':
            raise UserInactiveError(['User is not active or no has a role.'])

        if isinstance(learning_object_metadata, dict):
            if not ignore_schema:
                errors = is_valid_learning_object_metadata(
                    learning_object_metadata
                )
                if errors:
                    raise LearningObjectMetadataSchemaError(errors)

            # TODO: add files-path manager
            learning_object = new_learning_object(
                self.db, learning_object_metadata, user.get('_id')
            )
            errors = is_valid_learning_object(learning_object)
            if errors:
                raise LearningObjectSchemaError(errors)

            result = self.db.learning_objects.insert_one(
                learning_object
            )
            return result.inserted_id
        else:
            raise LearningObjectMetadataSchemaError()

    def get_one(self, _id, format_, user):
        """Get a learning object by _id."""
        # TODO: returns metadata or all object content?

        learning_object = self.db.learning_objects.find_one({'_id': _id})

        if user.get('role') != 'administrator':
            user_deleted = user.get('deleted')
            user_role = user.get('role')
            if user_deleted or user_role == 'unknown':
                raise UserInactiveError(
                    ['User is not active or no has a role.']
                )

            user_id = user.get('_id')
            if learning_object.get('user_id') != user_id:
                raise UserPermissionError(
                    ['User not have sufficient permissions to do this action.']
                )

        if not learning_object:
            raise LearningObjectNotFoundError(
                ['Learning Object _id not found.']
            )

        format_handler = {
            'xml': lambda lo: dict_to_xml(lo.get('metadata')),
            'json': lambda lo: lo.get('metadata')
        }

        if format_ not in format_handler.keys():
            raise LearningObjectFormatError(
                ['Format not found.']
            )

        return format_handler[format_](learning_object)

    def get_many(self, query):
        """Get learning objects with query."""
        if query and query.get('offset') and query.get('count'):
            try:
                offset = int(query.get('offset'))
                count = int(query.get('count'))
            except ValueError as e:
                raise ValueError(['Invalid offset or count parameters.'])
            search = query.get('search')
            if search:
                if only_letters(search):
                    fields_to_use = [
                        {x: {'$regex': f'.*{search}.*'}}
                        for x in [
                            'metadata.general.title',
                            # 'metadata.genetal.description'
                        ]
                    ]
                    query = {'$and': fields_to_use} if fields_to_use else {}
                    learning_objects = self.db.learning_objects.find(query)
                    return learning_objects.skip(offset).limit(count)
                else:
                    raise ValueError(['Invalid search value.'])
            return self.db.learning_objects.find().skip(offset).limit(count)
        else:
            raise ValueError(['Offset and Count required.'])

    def modify_one(self, _id, learning_object_metadata, user):
        """Modify learning object."""
        old_learning_object = self.db.learning_objects.find_one({'_id': _id})

        if user.get('role') != 'administrator':
            user_deleted = user.get('deleted')
            user_role = user.get('role')
            if user_deleted or user_role == 'unknown':
                raise UserInactiveError(
                    ['User is not active or no has a role.']
                )

            user_id = user.get('_id')
            if old_learning_object.get('user_id') != user_id:
                raise UserPermissionError(
                    ['User not have sufficient permissions to do this action.']
                )

        if not old_learning_object:
            raise LearningObjectNotFoundError({
                'errors': ['Learning Object _id not found.']
            })

        learning_object_schema = Definition(
            old_learning_object.get('schema')
        ).top()

        errors = learning_object_schema.validate(learning_object_metadata)

        if errors:
            raise LearningObjectMetadataSchemaError(errors)

        result = self.db.learning_objects.update_one(
            {'_id': _id},
            {'$set': {
                'metadata': learning_object_metadata,
                'modified': str(
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ),
            }}
        )
        if not result.modified_count:
            raise LearningObjectUnmodifyError(
                ['The Learning Object is not modified.']
            )

    def delete_one(self, _id, user):
        """Delete a learning object by _id."""
        learning_object = self.db.learning_objects.find_one({'_id': _id})

        if user.get('role') != 'administrator':
            user_deleted = user.get('deleted')
            user_role = user.get('role')
            if user_deleted or user_role == 'unknown':
                raise UserInactiveError(
                    ['User is not active or no has a role.']
                )

            user_id = user.get('_id')
            if learning_object.get('user_id') != user_id:
                raise UserPermissionError(
                    ['User not have sufficient permissions to do this action.']
                )

        if not learning_object:
            raise LearningObjectNotFoundError({
                'errors': ['Learning Object _id not found.']
            })
        result = self.db.learning_objects.delete_one({'_id': _id})
        if not result.deleted_count:
            raise LearningObjectUndeleteError(
                ['Learning Object is not deleted.']
            )
