from manager.exceptions.user import UserNotFoundError


def get_one(db_client, user_id, language):
    """Get a user by _id."""
    user = db_client.users.find_one(
        filter={'_id': user_id},
        projection=[
            'name',
            'email',
            'role',
            'status',
            'created',
            'modified',
            'deleted',
            'validated',
            'last_activity',
        ]
    )
    _ = language
    if not user:
        raise UserNotFoundError(_('User _id not found.'))
    user['id'] = user.get('_id')
    return user
