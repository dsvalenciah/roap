from uuid import uuid4
import typing
import json
import os

from schemas import User, Publication

from apistar import typesystem, Route, Include, Response, http
from apistar.frameworks.wsgi import WSGIApp as App

from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient(os.getenv('DB_HOST'), 27017)
db = client.roap

def create_user(user: http.RequestData) -> User:
    new_user = {
        '_id': uuid4().hex,
        'name': user.get('name'),
        'email': user.get('email')
    }

    result = db.users.insert_one(new_user)

    if not result.acknowledged:
        return Response(
            {'message': 'Error'}
        )

    return User(new_user)

def get_user(_id: typesystem.String) -> User:
    result = db.users.find_one({'_id': _id})
    if not result:
        return Response(
            {'message': 'The specified user _id not found'}
        )
    return User(json.loads(dumps(result)))

def get_all_users() -> Response:
    return Response(
        {'users': json.loads(dumps(db.users.find()))}
    )

def edit_user(_id: typesystem.String) -> Response:
    return Response(
        {'message': 'It works'}
    )

def delete_user(_id: typesystem.String) -> Response:
    return Response(
        {'message': 'It works'}
    )


user_routes = [
    Route('/', 'POST', create_user),
    Route('/{_id}', 'GET', get_user),
    Route('/', 'GET', get_all_users),
    Route('/{_id}', 'PUT', edit_user),
    Route('/{_id}', 'DELETE', delete_user)
]

ROUTES = [
    Include('/back/users', user_routes),
]


app = App(routes=ROUTES)
