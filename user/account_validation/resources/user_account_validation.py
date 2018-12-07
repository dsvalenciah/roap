
"""
Contains necessary Resources to works with user validation.
"""

import falcon
import jwt
import gettext
from bson.json_util import dumps


class UserValidate(object):
    """Deal with user validation."""

    def __init__(self, db):
        """Init."""
        self.db_client = db

    def on_get(self, req, resp, token):
        """Validate user."""
        _ = gettext.translation('account_validation', '/code/locale',
                                languages=[req.cookies.get('user_lang') or 'es_CO']).gettext

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
            resp.body = dumps({'message': [_('JWT token expired')]})
        except jwt.DecodeError as e:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = dumps({'message': [_('JWT decode error')]})
