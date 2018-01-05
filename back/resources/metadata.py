import json
import os
from uuid import uuid4
from datetime import datetime

from schemas.metadata import User
from utils.req_to_json import req_to_json

from pymongo import MongoClient
from bson.json_util import dumps

import falcon

client = MongoClient(os.getenv('DB_HOST'), 27017)
db = client.roap


class CreatorResource:
    def on_post(self, req, resp):
        item = req_to_json(req)
        item.update({
            '_id': str(uuid4().hex),
            'created': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        })

        valid_item, errors = item_schema.load(item)

        if errors:
            resp.body = json.dumps(errors)
            resp.status = falcon.HTTP_400
            return

        result = db.metadata.insert_one(valid_item)

        if not result.acknowledged:
            resp.body = {
                'message': 'Create item is not posible'
            }
            resp.status = falcon.HTTP_404
            return

        resp.status = falcon.HTTP_201
        resp.body = json.dumps(
            {'message': 'Ok', 'item': dumps(valid_item)}
        )

class ModifierResource:
    def on_put(self, req, resp, item_id):
        item = req_to_json(req)

        result = db.metadata.update_one(
            {'_id': item_id},
            {'$set': item}
        )

        if not result.modified_count:
            resp.body = {
                'message': 'The specified item id is not found on database'
            }
            resp.status = falcon.HTTP_404
            return

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'message': 'Ok'})

    def on_delete(self, req, resp, item_id):
        result = db.metadata.delete_one({'_id': item_id})
        if not result.deleted_count:
            resp.body = {
                'message': 'The specified item id is not found on database'
            }
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