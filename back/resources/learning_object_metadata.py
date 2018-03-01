
"""
Contains necessary Resources to works with learning-object metadata
fields CRUD operations.
"""

import json

from marshmallowjson.marshmallowjson import Definition
from marshmallowjson.exceptions import ValidationError
from utils.req_to_dict import req_to_dict
from utils.auth import Authenticate

from bson.json_util import dumps

import falcon


class LearningObjectMetadata(object):
    """Deal with the whole collection of learning-object-metadata-fields."""

    def __init__(self, db):
        """Init."""
        self.db = db

    @falcon.before(Authenticate())
    def on_get(self, req, resp, user):
        """Get a single learning-object-metadata-field."""
        if user.get('role') != 'Administrator':
            # Raise error
            pass

        result = self.db.learning_object_metadata.find_one({'_id': 'lom'})
        if not result:
            resp.status = falcon.HTTP_404
        else:
            resp.body = dumps(result)
            resp.status = falcon.HTTP_200

    @falcon.before(Authenticate())
    def on_put(self, req, resp, user):
        """Update learning-object-metadata-field."""
        if user.get('role') != 'Administrator':
            # Raise error
            pass

        lom = req_to_dict(req).get('lom')
        try:
            Definition(lom)
            result = self.db.learning_object_metadata.update_one(
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
