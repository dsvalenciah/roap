
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
from manager.utils.switch_language import SwitchLanguage

from manager.get_many import get_many
from manager.insert_one import insert_one

from bson.json_util import dumps

import falcon


@falcon.before(SwitchLanguage())
class UserCollection(object):
    """Deal with users."""

    def __init__(self, db):
        """Init."""
        self.db_client = db

    @falcon.before(Authenticate())
    def on_get(self, req, resp):
        """Get all users (maybe filtered, and paginated)."""
        query_params = {
            k: json.loads(v)
            for k, v in req.params.items()
        }
        try:
            auth_user = req.context.get('user')
            filter_ = query_params.get('filter', {})
            range_ = query_params.get('range', [0, 9])
            sorted_ = query_params.get('sort', ['id', 'desc'])
            users, total_count = get_many(
                db_client=self.db_client,
                filter_=filter_,
                range_=range_,
                sorted_=sorted_,
                auth_user=auth_user,
            )
            for user in users:
                user['id'] = user['_id']
            resp.body = dumps(users)
            len_users = len(users)
            resp.content_range = (
                range_[0],
                len_users - range_[0],
                total_count,
                'users'
            )
        except UserPermissionError as e:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})

    def on_post(self, req, resp):
        """Create user."""
        _ = req.context['user'].get('language')

        try:
            user = req_to_dict(req)
            _id = insert_one(
                db_client=self.db_client,
                user=user,
                language=_
            )
            resp.body = dumps({'_id': _id})
            resp.status = falcon.HTTP_201
        except UserDuplicateEmailError as e:
            resp.status = falcon.HTTP_CONFLICT
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except UserSchemaError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
