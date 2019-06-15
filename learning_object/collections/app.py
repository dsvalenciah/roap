
import os

import falcon
from falcon_cors import CORS

from pymongo import MongoClient


#from resources import LOCollection
from resources import LOCollectionCollection

class Roap():
    """Main Roap class."""

    def __init__(self,
                 db_host='DB_HOST', db_port='DB_PORT', db_name='DB_NAME'):
        """Create db and api for Roap."""
        self.client = MongoClient(os.getenv(db_host), int(os.getenv(db_port)))
        self.db = self.client[os.getenv(db_name)]

        self.api = falcon.API(middleware=[
            CORS(
                allow_all_origins=True,
                allow_all_methods=True,
                allow_all_headers=True,
                expose_headers_list=[
                    "Content-Range",
                ],
            ).middleware
        ])

        self.api.add_route(
            '/v1/collection', LOCollectionCollection(self.db)
        )
        """
        self.api.add_route(
            '/v1/collection/{_id}', LOCollection(self.db)
        )"""

    def get_db(self):
        """Obtain roap db."""
        return self.db

    def get_api(self):
        """Obtain roap api."""
        return self.api


roap = Roap()
api = roap.get_api()
