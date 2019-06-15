
"""
Contains necessary Resources to works with learning-objects CRUD operations.
"""

import json


from manager.exceptions.learning_object import (
    LearningObjectNotFoundError, LearningObjectSchemaError,
    LearningObjectUnmodifyError, LearningObjectUndeleteError,
    LearningObjectFormatError, LearningObjectMetadataSchemaError,
    InvalidUserRaterRole, InvalidRatingValue, UserCannotRate
)

from manager.exceptions.user import (
    UserInactiveError, UserPermissionError
)

from manager.utils.req_to_dict import req_to_dict
from manager.utils.auth import Authenticate
from manager.utils.switch_language import SwitchLanguage
from manager.get_one import get_one
from manager.modify_one import modify_one
from manager.delete_one import delete_one
from manager.rating_one import rating_one

from bson.json_util import dumps

import falcon


@falcon.before(SwitchLanguage())
class LearningObject(object):
    """Deal with single learning-object."""

    def __init__(self, db_client):
        """Init."""
        self.db_client = db_client

    @falcon.before(Authenticate())
    def on_get(self, req, resp, _id):
        """Get a single learning-object."""
        try:
            learning_object_format = req.params.get('format')
            user = req.context.get('user')
            learning_object = get_one(
                db_client=self.db_client,
                learning_object_id=_id,
                learning_object_format=learning_object_format,
                user=user,
            )
            if learning_object_format == 'xml':
                resp.content_type = 'text/xml'
                resp.body = learning_object
            else:
                resp.body = dumps(learning_object)
        except LearningObjectNotFoundError as e:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except LearningObjectFormatError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except UserInactiveError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except UserPermissionError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})

    @falcon.before(Authenticate())
    def on_put(self, req, resp, _id):
        """Update a single learning-object."""
        try:
            # TODO: validate new learning object schema.
            new_learning_object = req_to_dict(req)
            user = req.context.get('user')
            modify_one(
                db_client=self.db_client,
                old_learning_object_id=_id,
                new_learning_object=new_learning_object,
                user=user
            )
            resp.body = dumps({'data': {'id': _id}})
        except LearningObjectNotFoundError as e:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except LearningObjectSchemaError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0],  ensure_ascii=False)})
        except LearningObjectMetadataSchemaError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0],  ensure_ascii=False)})
        except UserInactiveError as e:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = dumps(
                {'message': json.dumps(e.args[0],  ensure_ascii=False)})
        except UserPermissionError as e:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = dumps(
                {'message': json.dumps(e.args[0],  ensure_ascii=False)})

    @falcon.before(Authenticate())
    def on_delete(self, req, resp, _id):
        """Delete a learing object (might be soft delete)."""
        try:
            user = req.context.get('user')
            delete_one(
                db_client=self.db_client,
                learning_object_id=_id,
                user=user,
            )
            resp.body = dumps({'status': 'deleted'})
        except LearningObjectNotFoundError as e:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except LearningObjectUndeleteError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except UserInactiveError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except UserPermissionError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})

    @falcon.before(Authenticate())
    def on_patch(self, req, resp, _id):
        """Rate a learning object."""
        # TODO: add exceptions.
        try:
            request = req_to_dict(req)
            user = req.context.get('user')
            rating = request.get('rating')
            rater_role = request.get('rater_role')
            rating_one(
                db_client=self.db_client,
                learining_object_id=_id,
                rater_role=rater_role,
                rating=rating,
                user=user,
            )
        except InvalidUserRaterRole as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except InvalidRatingValue as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except UserCannotRate as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
