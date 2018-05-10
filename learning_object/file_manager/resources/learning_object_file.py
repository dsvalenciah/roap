
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


from utils.auth import Authenticate

class LearningObjectFile(object):
    """Deal with learning object files."""

    @falcon.before(Authenticate())
    def on_post(self, req, resp):
        """Get learning object filer."""
        learning_object_file = req.get_param('file')
        file_extension = learning_object_file.filename.split('.')[-1]
        file_content = learning_object_file.file.read()

        storage = StorageUnit()

        result = storage.store(
            file_content,
            file_extension
        )

        result.update({
          "original_file_name": learning_object_file.filename,
        })

        try:
            resp.media = {
                "learningObjectFileMetadata": result,
                "contentType": FILE_MIME_TYPES.get(file_extension),
            }
        except FileNotFoundError:
            raise falcon.HTTPNotFound()