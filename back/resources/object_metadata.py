from datetime import datetime
from uuid import uuid4
import json
import re

from schemas.object_metadata import is_valid_schema_field
from utils.req_to_json import req_to_json

from bson.json_util import dumps

import falcon


only_letters = re.compile(r"^[A-Z]+$",re.IGNORECASE)

db = None

def set_db_client(db_client):
    global db
    db = db_client

def is_correct_parameter(param):
    return bool(only_letters.match(param))

class Create:
    def on_post(self, req, resp):
        if req.headers.get("AUTHORIZATION"):
            field = req_to_json(req)
            field.update({'_id': str(uuid4().hex)})
            valid_field, errors = is_valid_schema_field(field)
            if errors:
                resp.body = json.dumps(errors)
                resp.status = falcon.HTTP_400
            else:
                result = db.metadata.insert_one(field)
                if not result.acknowledged:
                    resp.status = falcon.HTTP_400
                else:
                    resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_401

class Modify:
    def on_put(self, req, resp, field_id):
        if req.headers.get("AUTHORIZATION"):
            field = req_to_json(req)

            result = db.metadata.update_one(
                {'_id': field_id},
                {'$set': field}
            )

            if not result.modified_count:
                resp.status = falcon.HTTP_404
            else:
                resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

    def on_delete(self, req, resp, field_id):
        if req.headers.get("AUTHORIZATION"):
            result = db.metadata.delete_one({'_id': field_id})
            if not result.deleted_count:
                resp.status = falcon.HTTP_404
            else:
                resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

class Query:
    def on_get(self, req, resp):
        if req.headers.get("AUTHORIZATION"):
            query_params = req.params
            if not query_params:
                resp.body = json.dumps(json.loads(dumps(db.metadata.find())))
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
                        db.metadata.find(query)
                    )))
                    resp.status = falcon.HTTP_200
                else:
                    resp.status = falcon.HTTP_400
        else:
            resp.status = falcon.HTTP_401


