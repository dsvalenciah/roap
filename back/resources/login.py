
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
            resp.body = json.dumps({'token': jwt.encode(
                {
                    'user_uid': user.get('_id'),
                    'exp': datetime.utcnow() + timedelta(seconds=3600),
                },
                'dsvalenciah_developer',
                algorithm='HS512'
            ).decode('utf-8')})
        else:
            resp.status = falcon.HTTP_400
            # TODO: show message with not sesion
