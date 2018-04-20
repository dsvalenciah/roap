
"""
Contains necessary Resources to works with learning object files.
"""

from utils.storage import StorageUnit

import falcon

class LearningObjectFile(object):
    """Deal with learning object files."""

    def on_get(self, req, resp, file_name):
        """Get learning object filer."""
        storage = StorageUnit()
        try:
            resp.stream = storage.open(file_name)
        except FileNotFoundError:
            raise falcon.HTTPNotFound()
