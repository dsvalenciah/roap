
"""
Contains roap app and his db run class.
"""

import os

from setup.compile_messages import create_mo_files

import falcon
from falcon_cors import CORS

from pymongo import MongoClient

from resources.user_account_validation import UserValidate
from resources.user_account_email import UserEmail


class Roap():
    """Main Roap class."""

    def __init__(self, db_host='DB_HOST', db_port='DB_PORT', db_name='DB_NAME'):
        """Create db and api for Roap."""
        self.client = MongoClient(os.getenv(db_host), int(os.getenv('DB_PORT')))
        self.db = self.client[os.getenv('DB_NAME')]

        create_mo_files()

        self.api = falcon.API(middleware=[
            CORS(
                allow_all_origins=True,
                allow_all_methods=True,
                allow_all_headers=True
            ).middleware
        ])

        self.api.add_route(
            '/v1/user-account/validate/{token}', UserValidate(self.db)
        )

        self.api.add_route(
            '/v1/user-account/send-email/{email}', UserEmail()
        )

    def get_db(self):
        """Obtain roap db."""
        return self.db

    def get_api(self):
        """Obtain roap api."""
        return self.api


roap = Roap()
api = roap.get_api()
