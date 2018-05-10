
"""
Contains necessary Resources to works with learning-objects CRUD operations.
"""

from random import randint

from manager.exceptions.learning_object import (
    LearningObjectNotFoundError, LearningObjectSchemaError,
    LearningObjectUnmodifyError, LearningObjectUndeleteError,
    LearningObjectFormatError, LearningObjectMetadataSchemaError
)

from manager.exceptions.user import (
    UserInactiveError, UserPermissionError
)

from manager.utils.req_to_dict import req_to_dict
from manager.utils.auth import Authenticate
from manager.get_one import get_one
from manager.modify_one import modify_one
from manager.delete_one import delete_one
from manager.rating_one import rating_one

from bson.json_util import dumps

import falcon


class LearningObject(object):
    """Deal with single learning-object."""

    def __init__(self, db_client):
        """Init."""
        self.db_client = db_client

    def on_get(self, req, resp, _id):
        """Get a single learning-object."""
        try:
            learning_object_format = req.params.get('format')
            user = req.context.get('user')
            learning_object = get_one(
                db_client=self.db_client,
                learning_object_id=_id,
                learning_object_format=learning_object_format,
                only_metadata=True,
            )
            resp.body = dumps(learning_object)
        except LearningObjectNotFoundError as e:
            raise falcon.HTTPNotFound(description=e.args[0])
        except LearningObjectFormatError as e:
            raise falcon.HTTPBadRequest(description=e.args[0])
        except UserInactiveError as e:
            raise falcon.HTTPUnauthorized(description=e.args[0])
        except UserPermissionError as e:
            raise falcon.HTTPUnauthorized(description=e.args[0])

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
                user=user,
            )
        except LearningObjectNotFoundError as e:
            raise falcon.HTTPNotFound(description=e.args[0])
        except LearningObjectMetadataSchemaError as e:
            raise falcon.HTTPError(description=e.args[0])
        except LearningObjectUnmodifyError as e:
            raise falcon.HTTPBadRequest(description=e.args[0])
        except UserInactiveError as e:
            raise falcon.HTTPUnauthorized(description=e.args[0])
        except UserPermissionError as e:
            raise falcon.HTTPUnauthorized(description=e.args[0])

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
        except LearningObjectNotFoundError as e:
            raise falcon.HTTPNotFound(description=e.args[0])
        except LearningObjectUndeleteError as e:
            raise falcon.HTTPBadRequest(description=e.args[0])
        except UserInactiveError as e:
            raise falcon.HTTPUnauthorized(description=e.args[0])
        except UserPermissionError as e:
            raise falcon.HTTPUnauthorized(description=e.args[0])

    @falcon.before(Authenticate())
    def on_patch(self, req, resp, _id):
        """Rate a learning object."""
        # TODO: add exceptions.
        try:
            user = req.context.get('user')
            rating = req.params.get('rating')
            rating_one(
                db_client=self.db_client,
                learining_object_id=_id,
                rating=rating,
                user=user,
            )
        except LearningObjectNotFoundError as e:
            raise falcon.HTTPNotFound(description=e.args[0])
        except LearningObjectUndeleteError as e:
            raise falcon.HTTPBadRequest(description=e.args[0])
        except UserInactiveError as e:
            raise falcon.HTTPUnauthorized(description=e.args[0])
        except UserPermissionError as e:
            raise falcon.HTTPUnauthorized(description=e.args[0])
