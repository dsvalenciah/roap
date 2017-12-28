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

def create_user(user: User) -> User:
    new_user = {
        '_id': uuid4().hex,
        'name': user.get('name'),
        'email': user.get('email')
    }
    new_user = User(new_user)

    result = db.users.insert_one(new_user)

    if not result.acknowledged:
        return Response(
            {'message': 'Create user is not posible'},
            status=404
        )

    return User(new_user)

def get_user(user_id: typesystem.String) -> User:
    result = db.users.find_one({'_id': user_id})
    if not result:
        return Response(
            {'message': 'The specified user id is not found on database'},
            status=404
        )
    return User(json.loads(dumps(result)))

def get_all_users() -> Response:
    return Response({'users': json.loads(dumps(db.users.find()))})

def modify_user(user_id: typesystem.String, user: User) -> Response:
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

def delete_user(user_id: typesystem.String) -> Response:
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

def create_publication(user_id: typesystem.String):
    return Response({'message': 'It Works!'})

def get_publication(user_id: typesystem.String, publ_id: typesystem.String):
    return Response({'message': 'It Works!'})

def get_publications(user_id: typesystem.String):
    return Response({'message': 'It Works!'})

def get_all_publications():
    return Response({'message': 'It Works!'})

def modify_publication(user_id: typesystem.String, publication: Publication):
    return Response({'message': 'It Works!'})

def delete_publication(user_id: typesystem.String, publ_id: typesystem.String):
    return Response({'message': 'It Works!'})

def delete_publications(user_id: typesystem.String):
    return Response({'message': 'It Works!'})

publication_routes = [
    # Create publication for the specified user id
    Route('/{user_id}', 'POST', create_publication),
    # Get publication by id for the specified user id
    Route('/{user_id}/{publ_id}', 'GET', get_publication),
    # Get all publications for the specified user id
    Route('/{user_id}', 'GET', get_publications),
    # Get all publications
    Route('/', 'GET', get_all_publications),
    # Modify publication by id for the specified user id
    Route('/{user_id}/{publ_id}', 'PUT', modify_publication),
    # Delete publication by id for the specified user id
    Route('/{user_id}/{publ_id}', 'DELETE', delete_publication),
    # Delete all publications for the specified user id
    Route('/{user_id}', 'DELETE', delete_publications),
]

ROUTES = [
    Include('/back/users', user_routes),
    Include('/back/publications', publication_routes),
]

app = App(routes=ROUTES)
