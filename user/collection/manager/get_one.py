from manager.exceptions.user import UserNotFoundError

def get_one(db_client, user_id):
    """Get a user by _id."""
    user = db_client.users.find_one({'_id': user_id})
    if not user:
        raise UserNotFoundError({
            'errors': ['User _id not found.']
        })
    return user