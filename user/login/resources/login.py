
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
            raise falcon.HTTPUnauthorized(description=['User not found.'])

        if not user.get('validated'):
            # User email is not validated.
            raise falcon.HTTPUnauthorized(
                description=['User email is not validated.']
            )

        if not user.get('aproved_by_admin'):
            # User is not validated by admin.
            raise falcon.HTTPUnauthorized(
                description=['User is not validated by admin.']
            )

        if user and sha512_crypt.verify(password, user.get('password')):
            token = jwt.encode(
                {
                    '_id': user.get('_id'),
                    'deleted': user.get('deleted'),
                    'validated': user.get('validated'),
                    'aproved_by_admin': user.get('aproved_by_admin'),
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
            # Incorrect password.
            raise falcon.HTTPUnauthorized(description=['Invalid password.'])
