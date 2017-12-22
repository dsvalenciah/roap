from apistar import typesystem, Route
from apistar.frameworks.wsgi import WSGIApp as App
from pymongo import MongoClient
import os

client = MongoClient(os.getenv('DB_STORAGE'), 27017)
db = client.test
names = db.names

def new():
    name_id = names.insert_one({'name': 'daniel'}).inserted_id
    return {'status': name_id}


ROUTES = [
    Route('/back/new', 'GET', new),
]

app = App(routes=ROUTES)
