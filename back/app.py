
"""
Contains roap app and his db run class.
"""

import os

from config.learning_object_metadata import learning_object_schema_populate
from config.collections_category import collections_category_populate

import falcon

from falcon_multipart.middleware import MultipartMiddleware

from pymongo import MongoClient

from resources import user
from resources import collections_category as cc
import resources.learning_object as lo
import resources.learning_object_metadata as lom


learning_object_schema_populate()
collections_category_populate()


class Roap():
    """Principal Roap class."""

    def __init__(self, db_host='DB_HOST', db_port=27017, db_name='roap'):
        """Create db and api for Roap."""
        self.client = MongoClient(os.getenv(db_host), db_port)
        self.db = self.client[db_name]

        lom.set_db_client(self.db)
        lo.set_db_client(self.db)
        user.set_db_client(self.db)
        cc.set_db_client(self.db)

        self.api = falcon.API(middleware=[MultipartMiddleware()])

        self.api.add_route('/back/user', user.UserCollection())
        self.api.add_route('/back/user/{uid}', user.User())

        self.api.add_route('/back/object', lo.LearningObjectCollection())
        self.api.add_route('/back/object/{uid}', lo.LearningObject())

        self.api.add_route('/back/object-meta', lom.LearningObjectMetadata())

        self.api.add_route('/back/collection', cc.CollectionsCategory())

    def get_db(self):
        """Obtain roap db."""
        return self.db

    def get_api(self):
        """Obtain roap api."""
        return self.api


roap = Roap()
api = roap.get_api()
