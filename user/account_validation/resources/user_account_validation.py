
"""
Contains necessary Resources to works with user validation.
"""
import os
import falcon
import jwt
import gettext
from bson.json_util import dumps
from utils.email_new_user_admin_notification import queue

class UserValidate(object):
    """Deal with user validation."""

    def __init__(self, db):
        """Init."""
        self.db_client = db

    def on_get(self, req, resp, token):
        """Validate user."""
        valid_langs = {
            'en_US': 'en_US',
            'es_CO': 'es_CO',
            'pt_BR': 'pt_BR'
        }
        value_lang_cookie = valid_langs.get(
            req.cookies.get('user_lang')) or 'es_CO'

        _ = gettext.translation('account_validation', '/code/locale',
                                languages=[value_lang_cookie]).gettext

        try:
            user = jwt.decode(
                token,
                os.getenv('JWT_SECRET'),
                verify='True',
                algorithms=['HS512'],
            )
            self.db_client.users.find_one_and_update(
                {'email': user.get('email')},
                {'$set': {'validated': True}},
            )
            queue().enqueue('utils.email_new_user_admin_notification.send_email')
        except jwt.ExpiredSignatureError as __:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = dumps({'message': [_('JWT token expired')]})
        except jwt.DecodeError as __:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = dumps({'message': [_('JWT decode error')]})
