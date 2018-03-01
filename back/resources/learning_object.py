
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
from utils.auth import Authenticate
from utils.learning_object import LearningObject as LearningObjectManager

from bson.json_util import dumps

import falcon


class LearningObject(object):
    """Deal with single learning-object."""

    def __init__(self, db):
        """Init."""
        self.db = db
        self.learning_object_manager = LearningObjectManager(self.db)

    @falcon.before(Authenticate())
    def on_get(self, req, resp, uid, user):
        """Get a single learning-object."""
        query_params = req.params
        format_ = query_params.get('format')
        try:
            learning_object = self.learning_object_manager.get_one(
                uid,
                format_,
                user
            )
            resp.body = dumps(learning_object)
        except LearningObjectNotFoundError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_404
        except LearningObjectFormatError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400

    @falcon.before(Authenticate())
    def on_put(self, req, resp, uid, user):
        """Update a single learning-object."""
        try:
            self.learning_object_manager.modify_one(
                uid,
                req_to_dict(req),
                user
            )
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

    @falcon.before(Authenticate())
    def on_delete(self, req, resp, uid, user):
        """Delete a learing object (might be soft delete)."""
        try:
            self.learning_object_manager.delete_one(
                uid,
                user
            )
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

    def __init__(self, db):
        """Init."""
        self.db = db
        self.learning_object_manager = LearningObjectManager(self.db)

    def on_get(self, req, resp):
        """Get all learning-objects (maybe filtered, and paginated)."""
        query_params = req.params
        try:
            learning_objects = self.learning_object_manager.get_many(
                query_params
            )
            resp.body = dumps(learning_objects)
        except ValueError as e:
            errors = e.args[0]
            resp.body = json.dumps({'errors': errors})
            resp.status = falcon.HTTP_400

    @falcon.before(Authenticate())
    def on_post(self, req, resp, user):
        """Create learning-object."""
        learning_object_metadata = None

        if req.content_type == 'application/json':
            learning_object_metadata = req_to_dict(req)
        elif req.content_type == 'text/xml':
            learning_object_metadata = xml_to_dict(req.stream.read())
        else:
            raise ValueError('Content-Type invalid')
            # TODO: Change exception type

        try:
            uid = self.learning_object_manager.insert_one(
                learning_object_metadata,
                user
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
