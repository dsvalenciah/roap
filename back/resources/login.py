
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
        if user and sha512_crypt.verify(password, user.get('password')):
            token = jwt.encode(
                {
                    '_id': user.get('_id'),
                    'deleted': user.get('deleted'),
                    'role': user.get('role'),
                    'name': user.get('name'),
                    'exp': datetime.utcnow() + timedelta(seconds=3600),
                },
                'dsvalenciah_developer',
                algorithm='HS512'
            ).decode('utf-8')
            resp.body = json.dumps({
                'token': token
            })
        elif not user:
            # User not exists
            raise falcon.HTTPBadRequest()
        else:
            # Incorrect password
            raise falcon.HTTPBadRequest()
