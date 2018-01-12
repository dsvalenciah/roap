import json
import re
from uuid import uuid4
from datetime import datetime

from schemas.user import is_valid_user
from utils.req_to_json import req_to_json

from bson.json_util import dumps
import pymongo

import falcon

only_letters = re.compile(r"^[A-Z]+$",re.IGNORECASE)

db = None


def set_db_client(db_client):
    global db
    db = db_client


def is_correct_parameter(param):
    return bool(only_letters.match(param))


class User(object):

    def on_get(self, req, res, uid):
        """
        Get a single user
        """

    def on_put(self, req, res, uid):
        """
        Update user
        """

    def on_delete(self, req, res, uid):
        """
        Delete single user
        """


class UserCollection(object):

    def on_get(self, req, res, uid):
        """
        Get all users (maybe filtered, and paginated)
        """

    def on_post(self, req, res):
        """
        Create user.
        """


class Create:
    def on_post(self, req, resp):
        if req.headers.get("AUTHORIZATION"):
            user = req_to_json(req)
            if not user.get('_id') and not user.get('created'):
                user.update({
                    '_id': str(uuid4().hex),
                    'created': str(
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    )
                })
            _, errors = is_valid_user(user)
            if errors:
                resp.body = json.dumps({"errors": errors})
                resp.status = falcon.HTTP_400
            else:
                try:
                    result = db.users.insert_one(user)
                    resp.status = falcon.HTTP_201
                except pymongo.errors.DuplicateKeyError:
                    resp.status = falcon.HTTP_400
        else:
            resp.status = falcon.HTTP_401

class Modify:
    def on_put(self, req, resp, user_id):
        if req.headers.get("AUTHORIZATION"):
            user = req_to_json(req)
            result = db.users.update_one(
                {'_id': user_id},
                {'$set': user}
            )
            if not result.modified_count:
                resp.body = json.dumps({
                    'message': 'The specified user id is not found on database'
                })
                resp.status = falcon.HTTP_404
            else:
                resp.status = falcon.HTTP_200
                resp.body = json.dumps({'message': 'Ok'})
        else:
            resp.status = falcon.HTTP_401

    def on_delete(self, req, resp, user_id):
        if req.headers.get("AUTHORIZATION"):
            result = db.users.delete_one({'_id': user_id})
            if not result.deleted_count:
                resp.body = json.dumps({
                    'message': 'The specified user id is not found on database'
                })
                resp.status = falcon.HTTP_404
            else:
                resp.status = falcon.HTTP_200
                resp.body = json.dumps({'message': 'Ok'})
        else:
            resp.status = falcon.HTTP_401

class Query:
    def on_get(self, req, resp):
        if req.headers.get("AUTHORIZATION"):
            query_params = req.params
            if not query_params:
                resp.body = json.dumps(json.loads(dumps(db.users.find())))
                resp.status = falcon.HTTP_200
            else:
                enabled_fields = [
                    "title", "description", "keyword", "name"
                ]
                correct_fields = map(
                    is_correct_parameter, query_params.values()
                )
                if not False in correct_fields:
                    fields_to_use = [
                        {x: {"$regex": f".*{query_params.get(x)}.*"}}
                        for x in query_params.keys()
                        if x in enabled_fields
                    ]
                    query = {"$and": fields_to_use}
                    resp.body = json.dumps(json.loads(dumps(
                        db.users.find(query)
                    )))
                    resp.status = falcon.HTTP_200
                else:
                    resp.status = falcon.HTTP_400
        else:
            resp.status = falcon.HTTP_401
