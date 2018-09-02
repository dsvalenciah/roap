from manager.exceptions.user import UserNotFoundError

def get_one(db_client, user_id):
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
    if not user:
        raise UserNotFoundError({
            'errors': ['User _id not found.']
        })
    user['id'] = user.get('_id')
    return user