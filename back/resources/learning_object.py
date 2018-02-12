
"""
Contains necessary Resources to works with learning-objects CRUD operations.
"""

from datetime import datetime
from uuid import uuid4
import re
import json

from schemas.learning_object_metadata import is_valid_learning_object_metadata
from schemas.learning_object import is_valid_learning_object
from utils.req_to_dict import req_to_dict
from utils.xml_to_dict import xml_to_dict
from utils.request_param import is_correct_parameter
from utils.dict_to_xml import dict_to_xml

from marshmallowjson.marshmallowjson import Definition

from bson.json_util import dumps

import falcon

db = None


def set_db_client(db_client):
    """Obtain db client."""
    global db
    db = db_client


class LearningObject(object):
    """Deal with single learning-object."""

    def on_get(self, req, resp, uid):
        """Get a single learning-object."""
        if req.headers.get('AUTHORIZATION'):
            query_params = req.params
            result = db.learning_objects.find_one({'_id': uid})
            if query_params.get('format') == 'xml':
                result = dict_to_xml(result.get('metadata'))
            if not result:
                resp.status = falcon.HTTP_404
            else:
                resp.body = dumps({"result": result})
                resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

    def on_put(self, req, resp, uid):
        """Update a single learning-object."""
        # Auth, check if the learing object belongs to the authorised user.
        if req.headers.get('AUTHORIZATION'):
            new_learning_object = req_to_dict(req)
            learning_object = db.learning_objects.find_one({'_id': uid})
            if not learning_object:
                resp.body = json.dumps(
                    {"loid": "specified lo uid is not valid"}
                )
                resp.status = falcon.HTTP_400
            else:
                learning_object_schema = Definition(
                    learning_object.get('schema')
                ).top()
                errors = learning_object_schema.validate(new_learning_object)
                if errors:
                    resp.body = json.dumps(
                        {'errors': errors, 'lo': new_learning_object}
                    )
                    resp.status = falcon.HTTP_400
                else:
                    result = db.learning_objects.update_one(
                        {'_id': uid},
                        {
                            '$set': {
                                'metadata': new_learning_object,
                                'modified': str(
                                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                ),
                            }
                        }
                    )
                    if not result.modified_count:
                        resp.status = falcon.HTTP_404
                    else:
                        resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

    def on_delete(self, req, resp, uid):
        """Delete a learing object (might be soft delete)."""
        if req.headers.get('AUTHORIZATION'):
            result = db.learning_objects.delete_one({'_id': uid})
            if not result.deleted_count:
                resp.status = falcon.HTTP_404
            else:
                resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401


class LearningObjectCollection(object):
    """Deal with the whole collection of learning-objects."""

    def on_get(self, req, resp):
        """Get all learning-objects (maybe filtered, and paginated)."""
        if req.headers.get('AUTHORIZATION'):
            query_params = req.params
            if not query_params:
                resp.body = dumps(db.learning_objects.find())
                resp.status = falcon.HTTP_200
            else:
                # TODO: add offset, count as a required params
                enabled_fields = [
                    # TODO: add 'start', 'end' date range
                    # get enabled fields depends on object schema
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
                        db.learning_objects.find(query)
                    )
                    resp.status = falcon.HTTP_200
                else:
                    resp.status = falcon.HTTP_400
        else:
            resp.status = falcon.HTTP_401

    def on_post(self, req, resp):
        """Create learning-object."""
        # Notice that, the user id will come in the payload
        if req.headers.get('AUTHORIZATION'):
            req_format = req.params.get('format') or 'json'

            learning_object_metadata = None
            user_id = None

            if req_format == 'xml':
                learning_object_metadata = xml_to_dict(
                    req.get_param('file').file.read()
                )
                user_id = req.get_param('user_id').value.decode()
            elif req_format == 'json':
                request_content = req_to_dict(req)
                learning_object_metadata = request_content.get('lom')
                user_id = request_content.get('user_id')

            if learning_object_metadata and user_id:
                errors = is_valid_learning_object_metadata(
                    learning_object_metadata
                )

                user = db.users.find_one({"_id": user_id})

                if not user:
                    errors.update(
                        {"userid": "specified user uid is not valid"}
                    )

                if user and user.get('status') != 'active':
                    errors.update(
                        {"userstatus": "specified user is not active"}
                    )

                if errors:
                    resp.body = json.dumps(
                        {'errors': errors, 'lom': learning_object_metadata}
                    )
                    resp.status = falcon.HTTP_400
                else:
                    # TODO: add files-path manager
                    learning_object = {
                        '_id': uuid4().hex,
                        'user_id': user.get('_id'),
                        'created': str(
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        ),
                        'modified': str(
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        ),
                        'schema': db.learning_object_metadata.find_one(
                            {'_id': 'lom'}
                        ).get('lom'),
                        'metadata': learning_object_metadata,
                        'state': "unevaluated",
                        'user_ranking': 0,
                        'evaluator_ranking': 0,
                        'files': [],
                    }
                    errors = is_valid_learning_object(learning_object)
                    if errors:
                        resp.body = json.dumps(
                            {'errors': errors, 'lo': learning_object}
                        )
                        resp.status = falcon.HTTP_400
                    else:
                        try:
                            result = db.learning_objects.insert_one(
                                learning_object
                            )
                            resp.status = falcon.HTTP_201
                        except pymongo.errors.DuplicateKeyError:
                            resp.status = falcon.HTTP_400
            else:
                resp.status = falcon.HTTP_400
        else:
            resp.status = falcon.HTTP_401
