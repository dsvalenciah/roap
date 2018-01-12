import json
import os

from resources import user
from resources import object_
from resources import object_metadata

from config.object_metadata import learning_object_schema_populate

import falcon

from pymongo import MongoClient

learning_object_schema_populate()

class Roap():
    def __init__(self, db_host='DB_HOST', db_port=27017, db_name="roap"):
        self.client = MongoClient(os.getenv(db_host), db_port)
        self.db = self.client[db_name]

        object_metadata.set_db_client(self.db)
        object_.set_db_client(self.db)
        user.set_db_client(self.db)

        self.api = falcon.API()

        self.api.add_route('/back/user', user.UserCollection())
        self.api.add_route('/back/user/{uid}', user.User())
        self.api.add_route('/back/object', object_.LearningObjectCollection())
        self.api.add_route('/back/object/{uid}', object_.LearningObject())

        self.api.add_route('/back/obj-meta', object_metadata.Query())
        self.api.add_route('/back/obj-meta-create', object_metadata.Create())
        self.api.add_route(
            '/back/obj-meta/{field_id}', object_metadata.Modify()
        )

        self.api.add_route('/back/obj', object_.Query())
        self.api.add_route('/back/obj-create/{user_id}', object_.Create())
        self.api.add_route('/back/obj/{user_id}/{object_id}', object_.Modify())

        self.api.add_route('/back/user', user.Query())
        self.api.add_route('/back/user-create', user.Create())
        self.api.add_route('/back/user/{user_id}', user.Modify())

    def get_db(self):
        return self.db

    def get_api(self):
        return self.api


roap = Roap()
api = roap.get_api()
