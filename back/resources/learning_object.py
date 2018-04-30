
"""
Contains necessary Resources to works with learning-objects CRUD operations.
"""

from random import randint

from exceptions.learning_object import (
    LearningObjectNotFoundError, LearningObjectSchemaError,
    LearningObjectUnmodifyError, LearningObjectUndeleteError,
    LearningObjectFormatError, LearningObjectMetadataSchemaError
)

from exceptions.user import (
    UserInactiveError, UserPermissionError
)

from utils.req_to_dict import req_to_dict
from utils.xml_to_dict import xml_to_dict
from utils.auth import Authenticate
from utils.learning_object import LearningObject as LearningObjectManager
from utils.learning_object import LearningObjectRating as LearningObjectRatingManager

from bson.json_util import dumps

import falcon


class LearningObject(object):
    """Deal with single learning-object."""

    def __init__(self, db):
        """Init."""
        self.learning_object_manager = LearningObjectManager(db)

    @falcon.before(Authenticate())
    def on_get(self, req, resp, _id):
        """Get a single learning-object."""
        query_params = req.params
        format_ = query_params.get('format')
        try:
            learning_object = self.learning_object_manager.get_one(
                _id,
                format_,
                req.context.get('user')
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
            self.learning_object_manager.modify_one(
                _id,
                req_to_dict(req),
                req.context.get('user')
            )
        except LearningObjectNotFoundError as e:
            raise falcon.HTTPNotFound(description=e.args[0])
        except LearningObjectMetadataSchemaError as e:
            raise falcon.HTTPError(
                falcon.HTTP_400, 'Metadata schema error', e.args[0]
            )
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
            self.learning_object_manager.delete_one(
                _id,
                req.context.get('user')
            )
        except LearningObjectNotFoundError as e:
            raise falcon.HTTPNotFound(description=e.args[0])
        except LearningObjectUndeleteError as e:
            raise falcon.HTTPBadRequest(description=e.args[0])
        except UserInactiveError as e:
            raise falcon.HTTPUnauthorized(description=e.args[0])
        except UserPermissionError as e:
            raise falcon.HTTPUnauthorized(description=e.args[0])


class LearningObjectRating(object):
    """Deal with single learning-object."""

    def __init__(self, db):
        """Init."""
        # TODO fix it
        self.learning_object_rating_manager = LearningObjectRatingManager(db)

    @falcon.before(Authenticate())
    def on_post(self, req, resp, _id):
        """Rate a learning object."""
        user = req.context.get('user')
        rating = req_to_dict(req).get('rating')
        self.learning_object_rating_manager.insert_one(_id, user, rating)

    def on_get(self, req, resp, _id):
        """Rate a learning object."""
        resp.body = dumps(self.learning_object_rating_manager.get_one(_id))


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
            raise falcon.HTTPBadRequest(description=e.args[0])

    @falcon.before(Authenticate())
    def on_post(self, req, resp):
        """Create learning-object."""
        # TODO: fix category
        # TODO: fix file manage
        import json
        learning_object_metadata = req.get_param('learningObjectMetadata')
        learning_object_file = req.get_param('file')
        file_extension = learning_object_file.filename.split('.')[-1]
        file_content = learning_object_file.file.read()

        try:
            learning_object_metadata = json.loads(learning_object_metadata)
        except:
            learning_object_metadata = xml_to_dict(req.stream.read())

        try:
            _id = self.learning_object_manager.insert_one(
                {
                    'lom': learning_object_metadata,
                    'category': [
                        "Educacion", "Medicina", "Fisica"
                    ][randint(0, 2)]
                },
                req.context.get('user'),
                {
                    'file_extension': file_extension,
                    'file_content': file_content
                }
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
