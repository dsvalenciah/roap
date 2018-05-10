
"""
Contains necessary Resources to works with user CRUD operations.
"""

from manager.exceptions.user import (
    UserNotFoundError, UserSchemaError, UserUnmodifyError, UserUndeleteError,
    UserDuplicateEmailError, UserPermissionError
)

from manager.utils.req_to_dict import req_to_dict
from manager.utils.auth import Authenticate

from manager.get_many import get_many
from manager.insert_one import insert_one

from bson.json_util import dumps

import falcon

class UserCollection(object):
    """Deal with users."""

    def __init__(self, db):
        """Init."""
        self.db_client = db

    @falcon.before(Authenticate())
    def on_get(self, req, resp):
        """Get all users (maybe filtered, and paginated)."""
        try:
            query_params = req.params
            auth_user = req.context.get('user')
            users = get_many(
                db_client=self.db_client,
                auth_user=auth_user,
                query=query_params,
            )
            resp.body = dumps(users)
        except UserPermissionError as e:
            raise falcon.HTTPUnauthorized(description=e.args[0])

    def on_post(self, req, resp):
        """Create user."""
        try:
            user = req_to_dict(req)
            _id = insert_one(
                db_client=self.db_client,
                user=user,
            )
            resp.body = dumps({'_id': _id})
            resp.status = falcon.HTTP_201
        except UserSchemaError as e:
            raise falcon.HTTPBadRequest(description=e.args[0])
        except UserDuplicateEmailError as e:
            raise falcon.HTTPBadRequest(description=e.args[0])