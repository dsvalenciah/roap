
"""
Contains utility functions to works with learning-object modify.
"""

from datetime import datetime

from manager.exceptions.learning_object import LearningObjectNotFoundError

from manager.exceptions.user import UserPermissionError

from manager.schemas.learning_object import LearningObject

from marshmallowjson.marshmallowjson import Definition

def check_user_permission(user, learning_object):
    learning_object_user_id = learning_object.get('user_id')
    user_id = user.get('_id')

    if user_id != learning_object_user_id:
        raise UserPermissionError(
            ['User is not own of this learning object.']
        )

def get_learning_object_metadata_schema(
        db_client, learning_object_metadata_schema_id):
    return db_client.lom_schema.find_one({
        '_id': learning_object_metadata_schema_id
    })

def modify_one(db_client, old_learning_object_id, new_learning_object, user):
    """Modify learning object."""
    old_learning_object = db_client.learning_objects.find_one({
        '_id': old_learning_object_id
    })

    if not old_learning_object:
        raise LearningObjectNotFoundError({
            'errors': ['Learning Object _id not found.']
        })

    check_user_permission(user, old_learning_object)

    old_learning_object_metadata_schema = get_learning_object_metadata_schema(
        db_client,
        old_learning_object.get('lom_schema_id')
    )

    LearningObjectMetadata = (
        Definition(old_learning_object_metadata_schema).top()
    )

    new_learning_object = LearningObject().dump(new_learning_object)

    new_learning_object_metadata = LearningObjectMetadata().dump(
        new_learning_object.get('metadata')
    )

    new_learning_object['modified'] = datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S'
    )

    result = db_client.learning_objects.update_one(
        {'_id': _id},
        {'$set': new_learning_object}
    )