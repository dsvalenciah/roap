import json
import os
from uuid import uuid4
from datetime import datetime

from schemas.metadata import is_valid_schema_field, is_valid_data
from utils.req_to_json import req_to_json

from pymongo import MongoClient
from bson.json_util import dumps

import falcon

client = MongoClient(os.getenv('DB_HOST'), 27017)
db = client.roap

class CreatorResource:
    def on_post(self, req, resp):
        field = req_to_json(req)
        field.update({'_id': str(uuid4().hex)})

        valid_field, errors = is_valid_schema_field(field)

        if errors:
            resp.body = json.dumps(errors)
            resp.status = falcon.HTTP_400
            return

        result = db.metadata.insert_one(valid_field)

        if not result.acknowledged:
            resp.body = json.dumps({
                'message': 'Create field is not posible'
            })
            resp.status = falcon.HTTP_404
            return

        resp.status = falcon.HTTP_201
        resp.body = json.dumps(
            {'message': 'Ok', 'field': dumps(valid_field)}
        )

class ModifierResource:
    def on_put(self, req, resp, field_id):
        field = req_to_json(req)

        result = db.metadata.update_one(
            {'_id': field_id},
            {'$set': field}
        )

        if not result.modified_count:
            resp.body = json.dumps({
                'message': 'The specified field id is not found on database'
            })
            resp.status = falcon.HTTP_404
            return

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'message': 'Ok'})

    def on_delete(self, req, resp, field_id):
        result = db.metadata.delete_one({'_id': field_id})
        if not result.deleted_count:
            resp.body = json.dumps({
                'message': 'The specified field id is not found on database'
            })
            resp.status = falcon.HTTP_404
            return

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'message': 'Ok'})

class FinderResource:
    def on_post(self, req, resp):
        query = req_to_json(req)
        if not query:
            resp.body = json.dumps(json.loads(dumps(db.metadata.find())))
            resp.status = falcon.HTTP_200
            return

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(query)

class ValidateLearningObject:
    def on_post(self, req, resp):
        data = req_to_json(req)

        valid_field, errors = is_valid_data(data)

        if errors:
            resp.body = json.dumps(errors)
            resp.status = falcon.HTTP_400
            return

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(
            {'message': 'Ok'}
        )