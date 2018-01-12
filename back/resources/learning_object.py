from datetime import datetime
from uuid import uuid4
import json

from schemas.object_metadata import is_valid_learning_object
from utils.req_to_json import req_to_json

from bson.json_util import dumps

import falcon


db = None


def set_db_client(db_client):
    global db
    db = db_client


class LearningObject(object):
    """
    Deal with single learning objects.
    """

    def on_get(self, req, res, uid):
        """
        Get a single learning object
        """

    def on_put(self, req, res, uid):
        """
        Update a single learning object
        """
        # Auth, check if the learing object belongs to the authorised user.

    def on_delete(self, req, res, uid):
        """
        Delete a learing object (might be soft delete)
        """


class LearningObjectCollection(object):
    """
    Deal with the whole collection of learning objects
    """


    def on_get(self, req, res):
        """
        Get all learning objects (maybe filtered, and paginated)
        """

    def on_post(self, req, res):
        """
        Create learning object.
        """
        # Notice that, the user id will come in the payload
        if req.headers.get("AUTHORIZATION"):
            learning_object = req_to_json(req)
            errors = is_valid_object(learning_object)
            if errors:
                resp.body = json.dumps({"errors": errors})
                resp.status = falcon.HTTP_400
            else:
                learning_object.update({'_id': uuid4().hex})
                try:
                    result = db.learning_objects.insert_one(learning_object)
                    resp.status = falcon.HTTP_201
                except pymongo.errors.DuplicateKeyError:
                    resp.status = falcon.HTTP_400
        else:
            resp.status = falcon.HTTP_401
