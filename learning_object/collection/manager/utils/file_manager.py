"""Abstract an storage unit."""
from zipfile import ZipFile
from uuid import uuid4
import base64
import os


class StorageUnit(object):
    """Abstraction for an storage unit."""

    def __init__(self, root=None):
        """Init."""
        if root is None:
            self.root = os.getenv('FILE_STORAGE')
        else:
            self.root = root

    def open(self, name, mode='rb'):
        """Open a file from the storage unit."""
        return open(self.path(name), mode)

    def path(self, name):
        """Create a path relative to the storage units root."""
        return os.path.join(self.root, name)

    def store(self, base64_file_content, file_metadata):
        """Store the file with a sha1 of its contents to avoid duplication."""
        # TODO: validata a filecontent.
        file_extension = file_metadata.get('extension')
        file_name = file_metadata.get('_id') + file_extension
        file_id = file_metadata.get('_id')
        with self.open(file_name, mode='wb') as file:
            file.write(base64.decodebytes(base64_file_content.encode("ascii")))

        if file_extension == '.zip':
            zip_ref = ZipFile(self.path(file_name), 'r')
            zip_ref.extractall(os.path.join(self.root, file_id))
            zip_ref.close()
