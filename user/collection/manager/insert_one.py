
from datetime import datetime
from uuid import uuid4

from manager.exceptions.user import (
    UserSchemaError, UserDuplicateEmailError
)

from passlib.hash import sha512_crypt

from manager.schemas.user import User

def new_user(name, email, password, requested_role):
    """Create a user dict."""
    # TODO: add salt to file configuration
    user = {
        '_id': str(uuid4()),
        'name': name,
        'password': sha512_crypt.hash(password, salt='dqwjfdsakuyfd'),
        'email': email,
        'role': requested_role,
        'aproved_by_admin': False,
        'created': datetime.now(),
        'modified': datetime.now(),
        'deleted': False,
        'last_activity': datetime.now(),
        'validated': False,
    }
    user, errors = User().dump(user)

    if errors:
        raise UserSchemaError(errors)

    return user

def insert_one(db_client, user):
    """Insert user."""
    # TODO: validate password and initial schema
    # TODO: add rq for process email sending
    # TODO: add resource for re try email sending if it fails
    if None in user.values():
        raise ValueError("Field not found.")

    user_with_similar_email = db_client.users.find_one(
        {'email': user.get('email')}
    )
    if user_with_similar_email:
        raise UserDuplicateEmailError({
            'error': 'Duplicate email.',
            'user_id': user_with_similar_email.get('_id')
        })

    user = new_user(
        user.get('name'),
        user.get('email'),
        user.get('password'),
        user.get('requested_role')
    )

    result = db_client.users.insert_one(user)

    return result.inserted_id
