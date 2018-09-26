
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
                {'email': user.get('email')},
                {'$set': {'validated': True}},
            )
        except jwt.ExpiredSignatureError as e:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = dumps({'message': ['JWT token expired']})
        except jwt.DecodeError as e:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = dumps({'message': ['JWT decode error']})
