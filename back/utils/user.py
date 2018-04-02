
"""
Contains utility functions to works with user.
"""


from datetime import datetime
from uuid import uuid4
import smtplib

import jwt

from exceptions.user import (
    UserNotFoundError, UserSchemaError, UserUnmodifyError, UserUndeleteError,
    UserDuplicateEmailError
)

from exceptions.user import (
    UserInactiveError, UserPermissionError
)

from schemas.user import is_valid_user

from passlib.hash import sha512_crypt


def new_user(name, email, password, requested_role):
    """Create a user dict."""
    # TODO: add salt to file configuration
    user = {
        '_id': str(uuid4().hex),
        'name': name,
        'password': sha512_crypt.hash(password, salt='dqwjfdsakuyfd'),
        'email': email,
        'role': 'unknown',
        'requested_role': requested_role,
        'created': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'modified': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'deleted': False,
        'last_activity': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'validated': False,
    }
    return user


class User():
    """docstring for User."""

    def __init__(self, db):
        """Init."""
        self.db = db

    def insert_one(self, user):
        """Insert user."""
        # TODO: validate password and initial schema
        # TODO: add rq for process email sending
        # TODO: add resource for re try email sending if it fails
        user_with_similar_email = self.db.users.find_one(
            {'email': user.get('email')}
        )
        if user_with_similar_email:
            raise UserDuplicateEmailError(['Duplicate email.'])

        user = new_user(
            user.get('name'),
            user.get('email'),
            user.get('password'),
            user.get('requested_role')
        )
        errors = is_valid_user(user)
        if errors:
            raise UserSchemaError(errors)

        result = self.db.users.insert_one(user)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        sender = 'roap.unal.master@gmail.com'
        receiver = user.get('email')
        server.login(sender, "@roap@unal@master")

        token = jwt.encode(
            {
                '_id': user.get('_id'),
            },
            'dsvalenciah_developer',
            algorithm='HS512'
        ).decode('utf-8')

        message = f"""
            From: Roap unal <{sender}>
            To: To Person <{receiver}>
            MIME-Version: 1.0
            Content-type: text/html
            Subject: Roap account validation
            <h1>Go to this link.</h1>
            <link>{token}</link>
        """

        server.sendmail(
            sender,
            "dsvalenciah@unal.edu.co",
            message
        )

        return result.inserted_id

    def get_one(self, _id, user):
        """Get a user by _id."""
        if user.get('role') != 'administrator':
            if _id != user.get('_id'):
                raise UserPermissionError(
                    ['User not have sufficient permissions to do this action.']
                )

        user = self.db.users.find_one({'_id': _id})
        if not user:
            raise UserNotFoundError({
                'errors': ['User _id not found.']
            })
        return user

    def get_many(self, query, user):
        """Get users with query."""
        # TODO: fix it and remove find().
        if user.get('role') != 'administrator':
            raise UserPermissionError(
                ['User not have sufficient permissions to do this action.']
            )

        if query and query.get('offset') and query.get('count'):
            try:
                offset = int(query.get('offset'))
                count = int(query.get('count'))
            except ValueError as e:
                raise ValueError(['Invalid offset or count parameters.'])
            enabled_fields = [
                'name', 'email', 'role', 'deleted', 'validated'
            ]
            if False not in enabled_fields:
                fields_to_use = [
                    {x: query.get(x)}
                    for x in query.keys()
                    if x in enabled_fields
                ]
                query = {'$and': fields_to_use} if fields_to_use else {}
                users = self.db.users.find(query)
                return users.skip(offset).limit(count)
            else:
                raise ValueError(['Invalid parameters value.'])
        else:
            return self.db.users.find()

    def modify_one(self, _id, user, auth_user):
        """Modify user."""
        # TODO: define who do modifies who
        # TODO: fix password
        if auth_user.get('role') != 'administrator':
            if _id != auth_user.get('_id'):
                raise UserPermissionError(
                    ['User not have sufficient permissions to do this action.']
                )

        old_user = self.db.users.find_one({'_id': _id})
        if not old_user:
            raise UserNotFoundError({
                'errors': ['User _id not found.']
            })

        user.update({
            '_id': old_user.get('_id'),
            'name': user.get('name') or old_user.get('name'),
            'password': user.get('password') or old_user.get('password'),
            'email': user.get('email') or old_user.get('email'),
            'role': user.get('role') or old_user.get('role'),
            'created': old_user.get('created'),
            'modified': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'deleted': user.get('deleted') or old_user.get('deleted'),
            'last_activity': old_user.get('last_activity'),
            'validated':  user.get('validated') or old_user.get('validated')
        })

        errors = is_valid_user(user)

        if errors:
            raise UserSchemaError(errors)

        result = self.db.users.update_one(
            {'_id': _id},
            {'$set': user}
        )

        if not result.modified_count:
            raise UserUnmodifyError(['The user is not modified.'])

    def delete_one(self, _id, user):
        """Delete a user by _id."""
        # TODO: Amind not self delete
        if user.get('role') != 'administrator':
            if _id != user.get('_id'):
                raise UserPermissionError(
                    ['User not have sufficient permissions to do this action.']
                )

        user = self.db.users.find_one({'_id': _id})
        if not user:
            raise UserNotFoundError({
                'errors': ['User _id not found.']
            })
        result = self.db.users.delete_one({'_id': _id})
        if not result.deleted_count:
            raise UserUndeleteError(['The user is not deleted.'])
