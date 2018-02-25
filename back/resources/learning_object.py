
"""
Contains necessary Resources to works with learning-objects CRUD operations.
"""

import json

from exceptions.learning_object import (
    LearningObjectNotFoundError, LearningObjectSchemaError,
    LearningObjectUnmodifyError, LearningObjectUndeleteError,
    LearningObjectFormatError, LearningObjectUserIdNotFound,
    LearningObjectMetadataSchemaError
)

from utils.req_to_dict import req_to_dict
from utils.xml_to_dict import xml_to_dict
from utils.authorization import Authorize
from utils.learning_object import LearningObject as LearningObjectManager

from bson.json_util import dumps

import falcon

db = None
learning_object_manager = None


def set_db_client(db_client):
    """Obtain db client."""
    global db
    global learning_object_manager
    db = db_client
    learning_object_manager = LearningObjectManager(db)


class LearningObject(object):
    """Deal with single learning-object."""

    @falcon.before(Authorize())
    def on_get(self, req, resp, uid):
        """Get a single learning-object."""
        query_params = req.params
        format_ = query_params.get('format')
        try:
            learning_object = learning_object_manager.insert_one(uid, format_)
            resp.body = dumps(learning_object)
        except LearningObjectNotFoundError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_404
        except LearningObjectFormatError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400

    @falcon.before(Authorize())
    def on_put(self, req, resp, uid):
        """Update a single learning-object."""
        try:
            learning_object_manager.modify_one(uid, req_to_dict(req))
        except LearningObjectNotFoundError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_404
        except LearningObjectMetadataSchemaError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400
        except LearningObjectUnmodifyError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400

    @falcon.before(Authorize())
    def on_delete(self, req, resp, uid):
        """Delete a learing object (might be soft delete)."""
        try:
            learning_object_manager.delete_one(uid)
        except LearningObjectNotFoundError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_404
        except LearningObjectUndeleteError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400


class LearningObjectCollection(object):
    """Deal with the whole collection of learning-objects."""

    def on_get(self, req, resp):
        """Get all learning-objects (maybe filtered, and paginated)."""
        query_params = req.params
        try:
            learning_objects = learning_object_manager.get_many(query_params)
            resp.body = dumps(learning_objects)
        except ValueError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400

    @falcon.before(Authorize())
    def on_post(self, req, resp):
        """Create learning-object."""
        # Notice that, the user id will come in the payload
        query_params = req.params
        format_ = query_params.get('format')

        learning_object_metadata = None
        user_id = None

        if format_ == 'xml':
            learning_object_metadata = xml_to_dict(
                req.get_param('file').file.read()
            )
            user_id = req.get_param('user_id').value.decode()
        elif format_ == 'json':
            request_content = req_to_dict(req)
            learning_object_metadata = request_content.get('lom')
            user_id = request_content.get('user_id')

        try:
            uid = learning_object_manager.insert_one(
                learning_object_metadata, user_id
            )
            resp.body = dumps({'uid': uid})
            resp.status = falcon.HTTP_201
        except LearningObjectMetadataSchemaError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400
        except LearningObjectUserIdNotFound as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400
        except LearningObjectSchemaError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400
