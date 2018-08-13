
from manager.exceptions.user import UserSchemaError, UserDuplicateEmailError

from manager.schemas.user import User

def insert_one(db_client, user):
    """Insert user."""
    # TODO: validate password and initial schema
    # TODO: add rq for process email sending
    # TODO: add resource for re try email sending if it fails
    user_with_similar_email = db_client.users.find_one(
        {'email': user.get('email')}
    )
    if user_with_similar_email:
        raise UserDuplicateEmailError([
            'User with speciffied email already exist.'
        ])

    user, errors = User().dump(user)

    if errors:
        raise UserSchemaError(errors)

    result = db_client.users.insert_one(user)

    return result.inserted_id
