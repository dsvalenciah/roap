
"""
Contains roap app and his db run class.
"""

import os

from config.learning_object_metadata import learning_object_schema_populate
from config.collections_category import collections_category_populate
from config.administrator import create_administrator
from config.learning_object import learning_object_populate

import falcon
from falcon_cors import CORS

from falcon_multipart.middleware import MultipartMiddleware

from pymongo import MongoClient

from resources import login
from resources import user
from resources import collections_category as cc
import resources.learning_object as lo
import resources.learning_object_metadata as lom


class Roap():
    """Main Roap class."""

    def __init__(self, db_host='DB_HOST', db_port=27017, db_name='roap'):
        """Create db and api for Roap."""
        self.client = MongoClient(os.getenv(db_host), db_port)
        self.db = self.client[db_name]

        learning_object_schema_populate(self.db)
        collections_category_populate(self.db)
        create_administrator(self.db)
        learning_object_populate(self.db)

        self.api = falcon.API(middleware=[
            MultipartMiddleware(),
            CORS(
                allow_all_origins=True,
                allow_all_methods=True,
                allow_all_headers=True
            ).middleware
        ])

        self.api.add_route('/back/login', login.Login(self.db))

        self.api.add_route('/back/user', user.UserCollection(self.db))
        self.api.add_route('/back/user/{_id}', user.User(self.db))

        self.api.add_route(
            '/back/object', lo.LearningObjectCollection(self.db)
        )
        self.api.add_route('/back/object/{_id}', lo.LearningObject(self.db))

        self.api.add_route(
            '/back/object-meta', lom.LearningObjectMetadata(self.db)
        )

        self.api.add_route('/back/collection', cc.CollectionsCategory(self.db))

    def get_db(self):
        """Obtain roap db."""
        return self.db

    def get_api(self):
        """Obtain roap api."""
        return self.api


roap = Roap()
api = roap.get_api()
