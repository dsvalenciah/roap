from uuid import uuid4
import typing
import json
import os

from apistar import Route, Response, http
from apistar.typesystem import String

from pymongo import MongoClient
from bson.json_util import dumps

from schemas import User

client = MongoClient(os.getenv('DB_HOST'), 27017)
db = client.roap

def create_user(user: User) -> typing.Union[User, Response]:
    user.update({'_id': uuid4().hex})

    result = db.users.insert_one(user)

    if not result.acknowledged:
        return Response(
            {'message': 'Create user is not posible'},
            status=404
        )

    return User(user)

def get_user(user_id: String) -> typing.Union[User, Response]:
    result = db.users.find_one({'_id': user_id})
    if not result:
        return Response(
            {'message': 'The specified user id is not found on database'},
            status=404
        )
    return User(json.loads(dumps(result)))

def get_all_users() -> Response:
    return Response({'users': json.loads(dumps(db.users.find()))})

def modify_user(user_id: String, user: User) -> Response:
    result = db.users.update_one(
        {'_id': user_id},
        {'$set': {'name': user.get('name'), 'email': user.get('email')}}
    )
    if not result.modified_count:
        return Response(
            {'message': 'The specified user id is not found on database'},
            status=404
        )
    return Response({'message': 'Modified'})

def delete_user(user_id: String) -> Response:
    result = db.users.delete_one({'_id': user_id})
    if not result.deleted_count:
        return Response(
            {'message': 'The specified user id is not found on database'},
            status=404
        )
    return Response({'message': 'Deleted'})


user_routes = [
    Route('/', 'POST', create_user), # Create new user
    Route('/{user_id}', 'GET', get_user), # Get user by user_id
    Route('/', 'GET', get_all_users), # Get all users into database
    Route('/{user_id}', 'PUT', modify_user), # Modify user by id
    Route('/{user_id}', 'DELETE', delete_user), # Delete user by id
]