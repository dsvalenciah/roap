from datetime import datetime
from uuid import uuid4
import re
import json

from schemas.learning_object_metadata import is_valid_learning_object
from utils.req_to_json import req_to_json
from utils.xml_to_json import xml_to_json
from utils.json_to_xml import json_to_xml

from bson.json_util import dumps

import falcon

only_letters = re.compile(r'^[A-Z]+$', re.IGNORECASE)
db = None


def set_db_client(db_client):
    global db
    db = db_client


def is_correct_parameter(param):
    return bool(only_letters.match(param))


class LearningObject(object):
    '''
    Deal with single learning objects.
    '''

    def on_get(self, req, resp, uid):
        '''
        Get a single learning object
        '''
        if req.headers.get('AUTHORIZATION'):
            result = db.learning_objects.find_one({'_id': uid})
            if not result:
                resp.status = falcon.HTTP_404
            else:
                resp.body = dumps(json_to_xml(result))
                resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

    def on_put(self, req, resp, uid):
        '''
        Update a single learning object
        '''
        # Auth, check if the learing object belongs to the authorised user.
        if req.headers.get('AUTHORIZATION'):
            learning_object = req_to_json(req)
            # TODO: validate new learning object
            result = db.learning_objects.update_one(
                {'_id': uid},
                {'$set': learning_object}
            )
            if not result.modified_count:
                resp.status = falcon.HTTP_404
            else:
                resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

    def on_delete(self, req, resp, uid):
        '''
        Delete a learing object (might be soft delete)
        '''
        if req.headers.get('AUTHORIZATION'):
            result = db.learning_objects.delete_one({'_id': uid})
            if not result.deleted_count:
                resp.status = falcon.HTTP_404
            else:
                resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401


class LearningObjectCollection(object):
    '''
    Deal with the whole collection of learning objects
    '''

    def on_get(self, req, resp):
        '''
        Get all learning objects (maybe filtered, and paginated)
        '''
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
        '''
        Create learning object.
        '''
        # Notice that, the user id will come in the payload
        if req.headers.get('AUTHORIZATION'):
            learning_object = req_to_json(req)
            if not learning_object:
                learning_object = xml_to_json(
                    req.get_param('xml_file').file.read()
                )
            errors = is_valid_learning_object(learning_object)
            user = db.users.find_one({"_id": learning_object.get('userid')})
            if errors or not user:
                errors.update(
                    {"userid": "specified user uid is not valid"}
                    if not user and not errors.get("userid") else {}
                )
                resp.body = json.dumps({'errors': errors, 'object': learning_object})
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
