
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
            raise falcon.HTTPMissingHeader("AUTHORIZATION")

        try:
            user = jwt.decode(
                authentication,
                'dsvalenciah_developer',
                verify='True',
                algorithms=['HS512'],
                # options={'verify_exp': True}
                # if you want to verify token (session) expiration, uncomment.
            )

            user_deleted = user.get('deleted')
            user_validated = user.get('validated')
            user_aproved_by_admin = user.get('status') == 'accepted'

            if user_deleted:
                raise falcon.HTTPUnauthorized('User deleted.')
            if not user_validated:
                raise falcon.HTTPUnauthorized('User not validated.')
            if not user_aproved_by_admin:
                raise falcon.HTTPUnauthorized('User unapproved.')

        except jwt.ExpiredSignatureError as e:
            raise falcon.HTTPUnauthorized('JWT expired', str(e))
        except jwt.DecodeError as e:
            raise falcon.HTTPUnauthorized('JWT decode error', str(e))

        req.context['user'] = {
            '_id': user.get('_id'),
            'role': user.get('role'),
        }
