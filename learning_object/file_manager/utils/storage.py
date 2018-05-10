"""Abstract an storage unit."""
from zipfile import ZipFile
from uuid import uuid4
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

    def store(self, file_content, file_extension):
        """Store the file with a sha1 of its contents to avoid duplication."""
        # TODO: validata a filecontent.
        file_id = str(uuid4())
        file_name = file_id + '.' + file_extension
        with self.open(file_name, 'wb') as file:
            file.write(file_content)

        if file_extension == 'zip':
            zip_ref = ZipFile(self.path(file_name), 'r')
            zip_ref.extractall(os.path.join(self.root, file_id))
            zip_ref.close()

        return {
            "file_name": file_name,
            "file_id": file_id,
            "file_extension": file_extension,
        }
