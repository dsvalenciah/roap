
"""
Contains necessary Resources to works with user CRUD operations.
"""

from exceptions.user import (
    UserNotFoundError, UserSchemaError, UserUnmodifyError, UserUndeleteError,
    UserDuplicateEmailError
)

from exceptions.user import UserPermissionError

from utils.req_to_dict import req_to_dict
from utils.auth import Authenticate
from utils.user import User as UserManager

from bson.json_util import dumps

import falcon


class User(object):
    """Deal with single user."""

    def __init__(self, db):
        """Init."""
        self.db = db
        self.user_manager = UserManager(self.db)

    @falcon.before(Authenticate())
    def on_get(self, req, resp, uid, user):
        """Get a single user."""
        try:
            user = self.user_manager.get_one(uid, user)
            resp.body = dumps(user)
        except UserNotFoundError as e:
            falcon.HTTPError(falcon.HTTP_404, 'Not found', e.args[0])
        except UserPermissionError as e:
            falcon.HTTPError(
                falcon.HTTP_401, 'User permission error', e.args[0]
            )

    @falcon.before(Authenticate())
    def on_put(self, req, resp, uid, user):
        """Update user."""
        try:
            self.user_manager.modify_one(uid, req_to_dict(req), user)
        except UserNotFoundError as e:
            falcon.HTTPError(falcon.HTTP_404, 'Not found', e.args[0])
        except UserSchemaError as e:
            falcon.HTTPError(falcon.HTTP_400, 'Schema error', e.args[0])
        except UserUnmodifyError as e:
            falcon.HTTPError(falcon.HTTP_400, 'Unmodify error', e.args[0])
        except UserPermissionError as e:
            falcon.HTTPError(
                falcon.HTTP_401, 'User permission error', e.args[0]
            )

    @falcon.before(Authenticate())
    def on_delete(self, req, resp, uid, user):
        """Delete single user."""
        # TODO: make cascade delete for all data related to this user
        try:
            self.user_manager.delete_one(uid, user)
        except UserNotFoundError as e:
            falcon.HTTPError(falcon.HTTP_404, 'Not found', e.args[0])
        except UserUndeleteError as e:
            falcon.HTTPError(falcon.HTTP_400, 'Undelete error', e.args[0])
        except UserPermissionError as e:
            falcon.HTTPError(
                falcon.HTTP_401, 'User permission error', e.args[0]
            )


class UserCollection(object):
    """Deal with the whole collection of learning-object-metadata-fields."""

    def __init__(self, db):
        """Init."""
        self.db = db
        self.user_manager = UserManager(self.db)

    @falcon.before(Authenticate())
    def on_get(self, req, resp, user):
        """Get all users (maybe filtered, and paginated)."""
        query_params = req.params
        try:
            users = self.user_manager.get_many(query_params, user)
            resp.body = dumps(users)
        except ValueError as e:
            falcon.HTTPError(
                falcon.HTTP_400, 'offset or count value error', e.args[0]
            )
        except UserPermissionError as e:
            falcon.HTTPError(
                falcon.HTTP_401, 'User permission error', e.args[0]
            )

    def on_post(self, req, resp):
        """Create user."""
        try:
            uid = self.user_manager.insert_one(req_to_dict(req))
            resp.body = dumps({'uid': uid})
            resp.status = falcon.HTTP_201
        except UserSchemaError as e:
            falcon.HTTPError(falcon.HTTP_400, 'Schema error', e.args[0])
        except UserDuplicateEmailError as e:
            falcon.HTTPError(
                falcon.HTTP_400, 'Duplicate email error', e.args[0]
            )
