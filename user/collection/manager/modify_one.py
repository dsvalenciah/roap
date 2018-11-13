
from datetime import datetime

from manager.exceptions.user import (
    UserPermissionError, UserNotFoundError, UserSchemaError
)

from manager.schemas.user import User

def modify_one(db_client, old_user_id, new_user, auth_user):
    """Modify user."""

    if auth_user.get('role') != 'administrator':
        if old_user_id != auth_user.get('_id'):
            raise UserPermissionError(
                'User not have sufficient permissions to do this action.'
            )

    old_user = db_client.users.find_one({'_id': old_user_id})

    if not old_user:
        raise UserNotFoundError('User _id not found.')

    new_user.update({
        'modified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    })

    new_user, errors = User(
        exclude=[
            '_id', 'password', 'email', 'created',
            'modified', 'validated', 'last_activity'
        ],
    ).dump(new_user)

    if errors:
        raise UserSchemaError(errors)

    db_client.users.update_one(
        {'_id': old_user_id},
        {'$set': new_user}
    )