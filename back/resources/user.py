
"""
Contains necessary Resources to works with user CRUD operations.
"""

import json
from uuid import uuid4
from datetime import datetime

from schemas.user import is_valid_user
from utils.req_to_dict import req_to_dict
from utils.request_param import is_correct_parameter

from bson.json_util import dumps
import pymongo

import falcon

db = None


def set_db_client(db_client):
    """Obtain db client."""
    global db
    db = db_client


class User(object):
    """Deal with single user."""

    def on_get(self, req, resp, uid):
        """Get a single user."""
        if req.headers.get('AUTHORIZATION'):
            result = db.users.find_one({'_id': uid})
            if not result:
                resp.status = falcon.HTTP_404
            else:
                resp.body = dumps(result)
                resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

    def on_put(self, req, resp, uid):
        """Update user."""
        if req.headers.get('AUTHORIZATION'):
            new_user = req_to_dict(req)
            # TODO: validate new user
            old_user = db.users.find_one({'_id': uid})
            if not old_user:
                resp.status = falcon.HTTP_404
            else:
                new_user.update({
                    '_id': old_user.get('_id'),
                    'created': old_user.get('created'),
                    'modified': str(
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ),
                    'last_activity': old_user.get('last_activity'),
                    'status': new_user.get('active') or old_user.get('status'),
                    'role': new_user.get('unknown') or old_user.get('role'),
                    'name': new_user.get('name') or old_user.get('name'),
                    'email': new_user.get('email') or old_user.get('email'),
                    'role': new_user.get('role') or old_user.get('role'),
                })
                errors = is_valid_user(new_user)

                if errors:
                    resp.body = json.dumps({'errors': errors})
                    resp.status = falcon.HTTP_400
                else:
                    result = db.users.update_one(
                        {'_id': uid},
                        {'$set': new_user}
                    )
                    if result.modified_count:
                        resp.status = falcon.HTTP_200
                    else:
                        resp.status = falcon.HTTP_404
        else:
            resp.status = falcon.HTTP_401

    def on_delete(self, req, resp, uid):
        """Delete single user."""
        # TODO: make cascade delete for all data related to this user
        if req.headers.get('AUTHORIZATION'):
            result = db.users.delete_one({'_id': uid})
            if not result.deleted_count:
                resp.status = falcon.HTTP_404
            else:
                resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401


class UserCollection(object):
    """Deal with the whole collection of learning-object-metadata-fields."""

    def on_get(self, req, resp):
        """Get all users (maybe filtered, and paginated)."""
        if req.headers.get('AUTHORIZATION'):
            query_params = req.params
            if not query_params:
                resp.body = dumps(db.users.find())
                resp.status = falcon.HTTP_200
            else:
                # TODO: add offset, count as a required params
                enabled_fields = [
                    'name', 'email', 'role', 'created', 'modified',
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
                        db.users.find(query)
                    )
                    resp.status = falcon.HTTP_200
                else:
                    resp.status = falcon.HTTP_400
        else:
            resp.status = falcon.HTTP_401

    def on_post(self, req, resp):
        """Create user."""
        if req.headers.get('AUTHORIZATION'):
            user = req_to_dict(req)
            user.update({
                '_id': str(uuid4().hex),
                'created': str(
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ),
                'modified': str(
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ),
                'last_activity': str(
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ),
                'status': 'active',
                'role': 'unknown',
            })
            errors = is_valid_user(user)
            if errors:
                resp.body = json.dumps({'errors': errors})
                resp.status = falcon.HTTP_400
            else:
                try:
                    result = db.users.insert_one(user)
                    resp.body = dumps({'uid': result.inserted_id})
                    resp.status = falcon.HTTP_201
                except pymongo.errors.DuplicateKeyError:
                    resp.status = falcon.HTTP_400
        else:
            resp.status = falcon.HTTP_401
