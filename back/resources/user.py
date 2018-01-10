import json
import os
from uuid import uuid4
from datetime import datetime

from schemas.user import is_valid_user
from utils.req_to_json import req_to_json

from pymongo import MongoClient
from bson.json_util import dumps

import falcon

client = MongoClient(os.getenv('DB_HOST'), 27017)
db = client.roap


class Create:
    def on_post(self, req, resp):
        if req.headers.get("AUTHORIZATION"):
            user = req_to_json(req)
            user.update({
                '_id': str(uuid4().hex),
                'created': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            })
            valid_user, errors = is_valid_user(user)
            if errors:
                resp.body = json.dumps({"errors": errors})
                resp.status = falcon.HTTP_400
            else:
                result = db.users.insert_one(valid_user)
                if not result.acknowledged:
                    resp.status = falcon.HTTP_400
                else:
                    resp.status = falcon.HTTP_201
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
