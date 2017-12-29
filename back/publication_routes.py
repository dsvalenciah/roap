from uuid import uuid4
import typing
import json
import os

from apistar import Route, Response, http
from apistar.typesystem import String

from pymongo import MongoClient
from bson.json_util import dumps

from schemas import Publication

def create_publication(user_id: String):
    return Response({'message': 'It Works yeah yeah!'})

def get_publication(user_id: String, publ_id: String):
    return Response({'message': 'It Works!'})

def get_publications(user_id: String):
    return Response({'message': 'It Works!'})

def get_all_publications():
    return Response({'message': 'It Works!'})

def modify_publication(user_id: String, publ_id: String, publ: Publication):
    return Response({'message': 'It Works!'})

def delete_publication(user_id: String, publ_id: String):
    return Response({'message': 'It Works!'})

def delete_publications(user_id: String):
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