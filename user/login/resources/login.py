
"""
Contains necessary Resources to works with user authentication.
"""

import json
from datetime import datetime, timedelta

from utils.req_to_dict import req_to_dict

import falcon
import jwt
from passlib.hash import sha512_crypt


class Login(object):
    """Deal with user authentication."""

    def __init__(self, db):
        """Init."""
        self.db = db

    def on_post(self, req, resp):
        """Authenticate user."""
        # TODO: add expiration seconds and secret to configuration file
        # TODO: create a login schema.
        # TODO: user has password?
        user = req_to_dict(req)
        email = user.get('email')
        password = user.get('password')
        user = self.db.users.find_one({'email': email})

        if not user:
            # User not exists.
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = json.dumps({'message': ['User not found.']})
            return

        if not user.get('validated'):
            # User email is not validated.
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = json.dumps(
                {'message': ['User email is not validated.']}
            )
            return

        if user.get('status') != 'accepted':
            # User is not validated by admin.
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = json.dumps({'message': ['User is not validated by admin.']})
            return

        if user and sha512_crypt.verify(password, user.get('password')):
            token = jwt.encode(
                {
                    '_id': user.get('_id'),
                    'deleted': user.get('deleted'),
                    'validated': user.get('validated'),
                    'status': user.get('status'),
                    'role': user.get('role'),
                    'name': user.get('name'),
                    # 'exp': datetime.utcnow() + timedelta(seconds=3600),
                },
                'dsvalenciah_developer',
                algorithm='HS512'
            ).decode('utf-8')
            resp.body = json.dumps({
                'token': token
            })
        else:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = json.dumps({'message': ['Invalid password.']})
            # Incorrect password.
