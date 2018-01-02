import json
import os
from uuid import uuid4
from datetime import datetime

from schemas import User

from pymongo import MongoClient
from bson.json_util import dumps

import falcon

client = MongoClient(os.getenv('DB_HOST'), 27017)
db = client.roap

user_schema = User()

def req_to_json(req):
    try:
        raw_json = req.stream.read()
    except Exception as ex:
        raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)

    try:
        result_json = json.loads(raw_json, encoding='utf-8')
    except ValueError:
        raise falcon.HTTPError(
            falcon.HTTP_400,
            'Malformed JSON',
            'Could not decode the request body. The '
            'JSON was incorrect.'
        )

    return result_json

class UserModifierResource:
    def on_put(self, req, resp, user_id):
        user = req_to_json(req)

        result = db.users.update_one(
            {'_id': user_id},
            {'$set': user}
        )

        if not result.modified_count:
            resp.body = {
                'message': 'The specified user id is not found on database'
            }
            resp.status = falcon.HTTP_404
            return

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'message': 'Ok'})

    def on_delete(self, req, resp, user_id):
        result = db.users.delete_one({'_id': user_id})
        if not result.deleted_count:
            resp.body = {
                'message': 'The specified user id is not found on database'
            }
            resp.status = falcon.HTTP_404
            return

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'message': 'Ok'})

class UserCreatorResource:
    def on_post(self, req, resp):
        user = req_to_json(req)
        user.update({
            '_id': str(uuid4().hex),
            'created': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        })

        valid_user, errors = user_schema.load(user)

        if errors:
            resp.body = json.dumps(errors)
            resp.status = falcon.HTTP_400
            return

        result = db.users.insert_one(valid_user)

        if not result.acknowledged:
            resp.body = {
                'message': 'Create user is not posible'
            }
            resp.status = falcon.HTTP_404
            return

        resp.status = falcon.HTTP_201
        resp.body = json.dumps(
            {'message': 'Ok', 'user': dumps(valid_user)}
        )

class UserFinderResource:
    def on_post(self, req, resp):
        query = req_to_json(req)
        if not query:
            resp.body = json.dumps(json.loads(dumps(db.users.find())))
            resp.status = falcon.HTTP_200
            return

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(query)


api = falcon.API()
api.add_route('/back/user/{user_id}', UserModifierResource())
api.add_route('/back/user-create', UserCreatorResource())
api.add_route('/back/user-search', UserFinderResource())