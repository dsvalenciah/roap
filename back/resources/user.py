
"""
Contains necessary Resources to works with user CRUD operations.
"""

import json

from exceptions.user import (
    UserNotFoundError, UserSchemaError, UserUnmodifyError, UserUndeleteError,
    UserDuplicateEmailError
)

from utils.req_to_dict import req_to_dict
from utils.authorization import Authorize
from utils.user import User as UserManager

from bson.json_util import dumps

import falcon

db = None
user_manager = None


def set_db_client(db_client):
    """Obtain db client."""
    global db
    global user_manager
    db = db_client
    user_manager = UserManager(db)


class User(object):
    """Deal with single user."""

    @falcon.before(Authorize())
    def on_get(self, req, resp, uid):
        """Get a single user."""
        try:
            user = user_manager.get_one(uid)
            resp.body = dumps(user)
        except UserNotFoundError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_404

    @falcon.before(Authorize())
    def on_put(self, req, resp, uid):
        """Update user."""
        try:
            user_manager.modify_one(uid, req_to_dict(req))
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

    @falcon.before(Authorize())
    def on_delete(self, req, resp, uid):
        """Delete single user."""
        # TODO: make cascade delete for all data related to this user
        try:
            user_manager.delete_one(uid)
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

    @falcon.before(Authorize())
    def on_get(self, req, resp):
        """Get all users (maybe filtered, and paginated)."""
        query_params = req.params
        try:
            users = user_manager.get_many(query_params)
            resp.body = dumps(users)
        except ValueError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400

    def on_post(self, req, resp):
        """Create user."""
        try:
            uid = user_manager.insert_one(req_to_dict(req))
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
