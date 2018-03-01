
"""
Contains necessary Resources to works with user CRUD operations.
"""

import json

from exceptions.user import (
    UserNotFoundError, UserSchemaError, UserUnmodifyError, UserUndeleteError,
    UserDuplicateEmailError
)

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
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_404

    @falcon.before(Authenticate())
    def on_put(self, req, resp, uid, user):
        """Update user."""
        try:
            self.user_manager.modify_one(uid, req_to_dict(req), user)
        except UserNotFoundError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_404
        except UserSchemaError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400
        except UserUnmodifyError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400

    @falcon.before(Authenticate())
    def on_delete(self, req, resp, uid, user):
        """Delete single user."""
        # TODO: make cascade delete for all data related to this user
        try:
            self.user_manager.delete_one(uid, user)
        except UserNotFoundError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_404
        except UserUndeleteError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400


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
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400

    def on_post(self, req, resp):
        """Create user."""
        try:
            uid = self.user_manager.insert_one(req_to_dict(req))
            resp.body = dumps({'uid': uid})
            resp.status = falcon.HTTP_201
        except UserSchemaError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400
        except UserDuplicateEmailError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400
