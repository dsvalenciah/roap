
"""
Contains necessary Resources to works with learning-object metadata
fields CRUD operations.
"""

import json

from marshmallowjson.marshmallowjson import Definition
from marshmallowjson.exceptions import ValidationError
from utils.req_to_dict import req_to_dict

from bson.json_util import dumps

import falcon


db = None


def set_db_client(db_client):
    """Obtain db client."""
    global db
    db = db_client


class LearningObjectMetadata(object):
    """Deal with the whole collection of learning-object-metadata-fields."""

    def on_get(self, req, resp):
        """Get a single learning-object-metadata-field."""
        if req.headers.get('AUTHORIZATION'):
            result = db.learning_object_metadata.find_one({'_id': 'lom'})
            if not result:
                resp.status = falcon.HTTP_404
            else:
                resp.body = dumps(result)
                resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

    def on_put(self, req, resp):
        """Update learning-object-metadata-field."""
        if req.headers.get('AUTHORIZATION'):
            lom = req_to_dict(req).get('lom')
            try:
                Definition(lom)
                result = db.learning_object_metadata.update_one(
                    {'_id': 'lom'},
                    {'$set': {'lom': lom}}
                )
                if not result.acknowledged:
                    resp.status = falcon.HTTP_400
                else:
                    resp.status = falcon.HTTP_201
            except ValidationError as e:
                resp.body = json.dumps({'errors': str(e)})
                resp.status = falcon.HTTP_400
        else:
            resp.status = falcon.HTTP_401
