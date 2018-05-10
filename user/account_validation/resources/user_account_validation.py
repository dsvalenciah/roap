
"""
Contains necessary Resources to works with user validation.
"""

import falcon
import jwt


class UserValidate(object):
    """Deal with user validation."""

    def __init__(self, db):
        """Init."""
        self.db_client = db

    def on_get(self, req, resp, token):
        """Validate user."""
        try:
            user = jwt.decode(
                token,
                'dsvalenciah_developer',
                verify='True',
                algorithms=['HS512'],
            )
            self.db_client.users.find_one_and_update(
                {'_id': user.get('_id')},
                {'$set': {'validated': True}},
            )
        except jwt.ExpiredSignatureError as e:
            raise falcon.HTTPUnauthorized('JWT token expired', str(e))
        except jwt.DecodeError as e:
            raise falcon.HTTPUnauthorized('JWT decode error', str(e))
