
"""
Contains necessary Resources to works with learning-objects CRUD operations.
"""

import json

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
from manager.insert_one import insert_one
from manager.insert_one import get_last_learning_object_metadata_schema_id
from manager.get_many import get_many

from bson.json_util import dumps

import falcon

class LearningObjectCollection(object):
    """Deal with the whole collection of learning-objects."""

    def __init__(self, db_client):
        """Init."""
        self.db_client = db_client

    def on_get(self, req, resp):
        """Get all learning-objects (maybe filtered, and paginated)."""
        query_params = {
            k: json.loads(v)
            for k, v in req.params.items()
        }
        try:
            filter_ = query_params.get('filter', {})
            range_ = query_params.get('range', [0,9])
            sorted_ = query_params.get('sort', ['id', 'desc'])
            learning_objects, total_count = get_many(
                db_client=self.db_client,
                filter_=filter_,
                range_=range_,
                sorted_=sorted_,
            )
            for learning_object in learning_objects:
                learning_object['id'] = learning_object['_id']
            resp.body = dumps(learning_objects)
            len_learning_objects = len(learning_objects)
            resp.content_range = (
                range_[0],
                len_learning_objects - range_[0],
                total_count,
                'learning-objects'
            )
        except ValueError as e:
            raise falcon.HTTPBadRequest(description=e.args[0])

    @falcon.before(Authenticate())
    def on_post(self, req, resp):
        """Create learning-object."""
        # TODO: fix category
        # TODO: fix file manage
        post_params = req_to_dict(req)
        metadata = post_params.get('metadata')
        category = post_params.get('category')
        # TODO: fix file format xml for example
        _format = post_params.get('format')
        base64_file = post_params.get('file')

        if None in [metadata, category, base64_file]:
            raise falcon.HTTPBadRequest(
                description=['An metadata, category, and file is required']
            )

        user = req.context['user']

        try:
            _id = insert_one(
                db_client=self.db_client,
                learning_object_metadata=metadata,
                learning_object_category=category,
                learning_object_format=_format or 'json',
                creator_id=user.get('_id'),
                learning_object_file=base64_file,
            )
            resp.body = dumps(
                {'_id': _id}
            )
            resp.status = falcon.HTTP_201
        except LearningObjectMetadataSchemaError as e:
            raise falcon.HTTPBadRequest(description=e.args[0])
        except LearningObjectSchemaError as e:
            raise falcon.HTTPBadRequest(description=e.args[0])
        except UserInactiveError as e:
            raise falcon.HTTPUnauthorized(description=e.args[0])