
"""
Contains utility functions to works with learning-object delete.
"""

from manager.exceptions.learning_object import LearningObjectNotFoundError
from manager.exceptions.user import UserPermissionError


def check_user_permission(user, learning_object):
    learning_object_creator = learning_object.get('creator_id')
    user_id = user.get('_id')
    _ = user.get('language')

    if user_id != learning_object_creator:
        raise UserPermissionError(
            _('User is not own of this learning object.'))


def delete_one(db_client, learning_object_id, user):
    """Delete a learning object by _id."""

    learning_object = db_client.learning_objects.find_one({
        '_id': learning_object_id
    })
    _id = learning_object_id
    _ = user.get('language')

    if not learning_object:
        raise LearningObjectNotFoundError(_('Learning Object _id not found.'))

    if user.get('role') != 'administrator':
        check_user_permission(user, learning_object)

    db_client.learning_objects.update_one(
        {'_id': _id},
        {'$set': {'deleted': True}},
    )
