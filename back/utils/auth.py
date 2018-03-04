
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
        if not authentication:
            falcon.HTTPMissingHeader("AUTHORIZATION")

        try:
            payload = jwt.decode(
                authentication,
                'dsvalenciah_developer',
                verify='True',
                algorithms=['HS512'],
                options={'verify_exp': True}
            )
        except jwt.ExpiredSignatureError as e:
            raise falcon.HTTPUnauthorized('JWT token expired', str(e))
        except jwt.DecodeError as e:
            raise falcon.HTTPUnauthorized('JWT decode error', str(e))

        req.context['user'] = {
            '_id': payload.get('_id'),
            'deleted': payload.get('deleted'),
            'role': payload.get('role'),
        }
