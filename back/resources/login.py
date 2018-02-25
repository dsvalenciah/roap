
"""
Contains necessary Resources to works with user authentication.
"""

import json
from datetime import datetime, timedelta

from utils.req_to_dict import req_to_dict

import falcon
import jwt
from passlib.hash import sha512_crypt


db = None


def set_db_client(db_client):
    """Obtain db client."""
    global db
    db = db_client


class Login(object):
    """Deal with user authentication."""

    def on_post(self, req, resp):
        """Authenticate user."""
        # TODO: add expiration seconds and secret to configuration file
        # TODO: user has password?
        user = req_to_dict(req)
        email = user.get('email')
        password = user.get('password')
        user = db.users.find_one({'email': email})
        if user and sha512_crypt.verify(password, user.get('password')):
            resp.body = json.dumps({'token': jwt.encode(
                {
                    'uid': user.get('_id'),
                    'role': user.get('role'),
                    'status': user.get('status'),
                    'exp': datetime.utcnow() + timedelta(seconds=3600),
                },
                'dsvalenciah_developer',
                algorithm='HS512'
            ).decode('utf-8')})
        else:
            resp.status = falcon.HTTP_400
            # TODO: show message with not sesion
