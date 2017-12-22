from apistar import typesystem, Route
from apistar.frameworks.wsgi import WSGIApp as App
from pymongo import MongoClient
from bson.json_util import dumps
import json
import os

client = MongoClient(os.getenv('DB_HOST'), 27017)
db = client.test
names = db.names


def new():
    name_id = names.insert_one({'name': 'daniel'}).inserted_id
    return {'name_id': str(name_id), 'db': json.loads(dumps(names.find()))}


ROUTES = [
    Route('/back/new', 'GET', new),
]

app = App(routes=ROUTES)
