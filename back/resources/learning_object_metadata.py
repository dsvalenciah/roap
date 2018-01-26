
"""
Contains necessary Resources to works with learning-object metadata
fields CRUD operations.
"""

from datetime import datetime
from uuid import uuid4
import json
import re

from schemas.learning_object_metadata import is_valid_schema_field
from utils.req_to_dict import req_to_dict
from utils.request_param import is_correct_parameter

from bson.json_util import dumps

import falcon


db = None


def set_db_client(db_client):
    """Obtain db client."""
    global db
    db = db_client


class LearningObjectMetadata(object):
    """Deal with single learning-object-metadata-field."""

    def on_get(self, req, resp, uid):
        """Get a single learning-object-metadata-field."""
        if req.headers.get('AUTHORIZATION'):
            result = db.learning_object_metadata.find_one(
                {'_id': uid}
            )
            if not result:
                resp.status = falcon.HTTP_404
            else:
                resp.body = dumps(result)
                resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

    def on_put(self, req, resp, uid):
        """Update learning-object-metadata-field."""
        if req.headers.get('AUTHORIZATION'):
            field = req_to_dict(req)
            # TODO: validate new learning-object-metadata-field
            result = db.learning_object_metadata.update_one(
                {'_id': uid},
                {'$set': field}
            )

            if not result.modified_count:
                resp.status = falcon.HTTP_404
            else:
                resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

    def on_delete(self, req, resp, uid):
        """Delete single learning-object-metadata-field."""
        if req.headers.get('AUTHORIZATION'):
            result = db.learning_object_metadata.delete_one(
                {'_id': uid}
            )
            if not result.deleted_count:
                resp.status = falcon.HTTP_404
            else:
                resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401


class LearningObjectMetadataCollection(object):
    """Deal with the whole collection of learning-object-metadata-fields."""

    def on_get(self, req, resp):
        """Get all users (maybe filtered, and paginated)."""
        if req.headers.get('AUTHORIZATION'):
            query_params = req.params
            if not query_params:
                resp.body = dumps(
                    db.learning_object_metadata.find()
                )
                resp.status = falcon.HTTP_200
            else:
                # TODO: add offset, count as a required params
                enabled_fields = [
                    'title', 'description', 'keyword', 'name'
                    # TODO: add 'start', 'end' date range
                    # add 'offset', 'count'
                ]
                correct_fields = map(
                    is_correct_parameter, query_params.values()
                )
                if False not in correct_fields:
                    fields_to_use = [
                        {x: {'$regex': f'.*{query_params.get(x)}.*'}}
                        for x in query_params.keys()
                        if x in enabled_fields
                    ]
                    query = {'$and': fields_to_use}
                    resp.body = dumps(
                        db.learning_object_metadata.find(query)
                    )
                    resp.status = falcon.HTTP_200
                else:
                    resp.status = falcon.HTTP_400
        else:
            resp.status = falcon.HTTP_401

    def on_post(self, req, resp):
        """Create learning-object-metadata-field."""
        if req.headers.get('AUTHORIZATION'):
            field = req_to_dict(req)
            field.update({'_id': str(uuid4().hex)})
            errors = is_valid_schema_field(field)
            if errors:
                resp.body = json.dumps({'errors': errors})
                resp.status = falcon.HTTP_400
            else:
                result = db.learning_object_metadata.insert_one(field)
                if not result.acknowledged:
                    resp.status = falcon.HTTP_400
                else:
                    resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_401
