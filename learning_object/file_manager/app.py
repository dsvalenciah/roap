
"""
Contains roap learning object file manager.
"""

import os

import falcon
from falcon_cors import CORS

from falcon_multipart.middleware import MultipartMiddleware

from resources.learning_object_file import LearningObjectFile

class Roap():
    """Main Roap file manager class."""

    def __init__(self):
        """Create api for Roap."""
        self.api = falcon.API(middleware=[
            MultipartMiddleware(),
            CORS(
                allow_all_origins=True,
                allow_all_methods=True,
                allow_all_headers=True
            ).middleware
        ])

        self.api.add_route(
            '/v1/learning-object-file-manager', LearningObjectFile()
        )

    def get_api(self):
        """Obtain roap api."""
        return self.api


roap = Roap()
api = roap.get_api()
