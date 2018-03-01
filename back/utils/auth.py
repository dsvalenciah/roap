
"""
Contains utility functions to works with Authentication.
"""

import jwt
import falcon


class Authenticate(object):
    """Deal with the user Authentication."""

    def __init__(self):
        """Init."""

    def __call__(self, req, resp, resource, params):
        """Authorize request."""
        # TODO: get secret from configuration file and fix raise errors
        authentication = req.headers.get('AUTHORIZATION')
        db = resource.db

        try:
            payload = jwt.decode(
                authentication,
                'dsvalenciah_developer',
                verify='True',
                algorithms=['HS512'],
                options={'verify_exp': True}
            )
        except jwt.ExpiredSignatureError as e:
            raise falcon.HTTPUnauthorized('Expired', str(e))
        except jwt.DecodeError as e:
            raise falcon.HTTPUnauthorized('Decode error', str(e))

        user_uid = payload.get('user_uid')

        params['user'] = db.users.find_one({'_id': user_uid})
