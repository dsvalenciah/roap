
"""
Contains necessary Resources to works with user CRUD operations.
"""

import json
import gettext
from manager.exceptions.user import (
    UserNotFoundError, UserSchemaError, UserUnmodifyError, UserUndeleteError,
    UserDuplicateEmailError, UserPermissionError
)

from manager.utils.req_to_dict import req_to_dict
from manager.utils.auth import Authenticate

from manager.get_one import get_one
from manager.modify_one import modify_one
from manager.delete_one import delete_one

from bson.json_util import dumps
from manager.utils.switch_language import SwitchLanguage
import falcon

# TODO: password pattern

@falcon.before(SwitchLanguage())
class User(object):
    """Deal with single user."""

    def __init__(self, db):
        """Init."""
        self.db_client = db

    def on_get(self, req, resp, _id):
        """Get a single user."""
        _ = req.context.get('user').get('language')
        try:
            user = get_one(
                db_client=self.db_client,
                user_id=_id,
                language=_
            )
            resp.body = dumps(user)
        except UserNotFoundError as e:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except UserPermissionError as e:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})

    @falcon.before(Authenticate())
    def on_put(self, req, resp, _id):
        """Update user."""
        try:
            new_user = req_to_dict(req)
            auth_user = req.context.get('user')
            modify_one(
                db_client=self.db_client,
                old_user_id=_id,
                new_user=new_user,
                auth_user=auth_user,
            )
            resp.body = dumps({'data': new_user})
        except UserNotFoundError as e:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except UserSchemaError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except UserUnmodifyError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except UserPermissionError as e:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})

    @falcon.before(Authenticate())
    def on_delete(self, req, resp, _id):
        """Delete single user."""
        # TODO: make cascade delete for all data related to this user
        try:
            auth_user = req.context.get('user')
            delete_one(
                db_client=self.db_client,
                user_id=_id,
                auth_user=auth_user,
            )
            resp.body = dumps({'status': 'deleted'})
        except UserNotFoundError as e:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except UserUndeleteError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except UserPermissionError as e:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
