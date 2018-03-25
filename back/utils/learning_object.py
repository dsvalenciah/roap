
"""
Contains utility functions to works with learning-objects.
"""


from datetime import datetime
# TODO: use utcnow()
import json
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

from bson.json_util import dumps


def new_learning_object(
        db, learning_object_metadata, user_id, category, _id=None):
    """Create a learning object dict."""
    # TODO: add salt to file configuration

    learning_object = {
        '_id': uuid4().hex if not _id else _id,
        'user_id': user_id,
        'lom_schema_id': json.loads(dumps(
            db.lom_schema.find().sort("created", -1).limit(1)
        ))[0].get('_id'),
        'category': category,
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'modified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'deleted': False,
        'evaluated': False,
        'metadata': learning_object_metadata,
        'files_path': [],
    }
    return learning_object


class LearningObjectScore():
    """docstring for Learning Object Rate."""

    def __init__(self, db):
        """Init."""
        self.db = db

    def insert_one(self, _id, user, score):
        """Rate a learning object."""
        # TODO: fix it
        self.db.learning_object_score.insert_one({
            '_id': _id + '_' + user.get('_id'),
            'learning_object_id': _id,
            'user_id': user.get('_id'),
            'score': score,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_role': user.get('role'),
        })

    def get_one(self, _ids):
        """Rate a learning object."""
        # TODO: fix it
        pipe = [
            {"$match": {"$or": [
                {"learning_object_id": _id}
                for _id in _ids
            ]}},
            {
                '$group': {
                    '_id': {
                        "learning_object_id": "$learning_object_id",
                        'user_role': '$user_role'
                    },
                    'total': {'$avg': '$score'},
                },
            }
        ]
        learning_object_scores = self.db.learning_object_score.aggregate(
            pipeline=pipe
        )
        result = {
            los.get('_id', {}).get('learning_object_id'): {
                los.get('_id', {}).get('user_role'): los.get('total')
            }
            for los in learning_object_scores
        }
        return result


class LearningObject():
    """docstring for Learning Object."""

    def __init__(self, db):
        """Init."""
        self.db = db
        self.learning_object_score_manager = LearningObjectScore(db)

    def insert_one(self, learning_object, user, ignore_schema=False, _id=None):
        """Insert learning object."""
        user_deleted = user.get('deleted')
        user_role = user.get('role')
        if user_deleted or user_role == 'unknown':
            raise UserInactiveError(['User is not active or no has a role.'])

        learning_object_metadata = learning_object.get('lom')
        category = learning_object.get('category')

        if isinstance(learning_object_metadata, dict):
            if not ignore_schema:
                errors = is_valid_learning_object_metadata(
                    learning_object_metadata
                )
                if errors:
                    raise LearningObjectMetadataSchemaError(errors)

            # TODO: add files-path manager
            # TODO: add correct category
            learning_object = new_learning_object(
                self.db,
                learning_object_metadata,
                user.get('_id'),
                category,
                _id
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
