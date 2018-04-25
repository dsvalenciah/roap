
"""
Contains necessary Resources to works with learning object files.
"""

from utils.storage import StorageUnit

import falcon


# TODO: add another ppt file format

FILE_MIME_TYPES = {
  'zip': 'application/zip',
  'pdf': 'application/pdf',
  'png': 'image/png',
  'jpg': 'image/jpeg',
  'mp4': 'video/mp4',
  'mpg': 'audio/mpeg',
  'doc': 'application/msword',
  'ppt': 'application/vnd.ms-powerpoint',
};


class LearningObjectFile(object):
    """Deal with learning object files."""

    def on_get(self, req, resp, file_name):
        """Get learning object filer."""
        storage = StorageUnit()
        try:
            file_extension = file_name.split(".")[-1]
            resp.media = {
                "url": storage.path(file_name),
                "extension": file_extension,
                "contentType": FILE_MIME_TYPES.get(file_extension)
            }
        except FileNotFoundError:
            raise falcon.HTTPNotFound()
