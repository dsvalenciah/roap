
"""
Contains necessary Resources to works with user validation.
"""

from utils.user import User as UserManager

import falcon
import jwt


class UserValidate(object):
    """Deal with user validation."""

    def __init__(self, db):
        """Init."""
        self.user_manager = UserManager(db)

    def on_get(self, req, resp, token):
        """Validate user."""
        try:
            user = jwt.decode(
                token,
                'dsvalenciah_developer',
                verify='True',
                algorithms=['HS512'],
            )
            self.user_manager.modify_one(
                user.get('_id'),
                {'validated': True},
                user
            )
        except jwt.ExpiredSignatureError as e:
            raise falcon.HTTPUnauthorized('JWT token expired', str(e))
        except jwt.DecodeError as e:
            raise falcon.HTTPUnauthorized('JWT decode error', str(e))
        except UserNotFoundError as e:
            raise falcon.HTTPNotFound(description=e.args[0])
        except UserSchemaError as e:
            raise falcon.HTTPBadRequest(description=e.args[0])
        except UserUnmodifyError as e:
            raise falcon.HTTPBadRequest(description=e.args[0])
        except UserPermissionError as e:
            raise falcon.HTTPUnauthorized(description=e.args[0])


