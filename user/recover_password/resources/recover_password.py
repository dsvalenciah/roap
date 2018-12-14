import falcon
import jwt
import gettext
import os
from bson.json_util import dumps
from utils.req_to_dict import req_to_dict
from passlib.hash import sha512_crypt
from utils.switch_language import SwitchLanguage


@falcon.before(SwitchLanguage())
class UserRecoverPassword(object):
    def __init__(self, db):
        self.db_client = db

    def on_post(self, req, resp, token):
        _ = req.context.get('language')
        new_password = req_to_dict(req).get('password')
        encrypted_password = sha512_crypt.hash(
            new_password,
            salt=os.getenv('SALT')
        )

        try:
            user = jwt.decode(
                token,
                os.getenv('JWT_SECRET'),
                verify='True',
                algorithms=['HS512']
            )

            self.db_client.users.find_one_and_update(
                {'email': user.get('email')},
                {'$set': {'password': encrypted_password}}
            )

            resp.status = falcon.HTTP_200
            resp.body = dumps(
                {'message': [_('Your password has been changed')]})
        except jwt.ExpiredSignatureError as e:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = dumps({'message': [_('JWT token expired')]})
        except jwt.DecodeError as e:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = dumps({'message': [_('JWT decode error')]})
