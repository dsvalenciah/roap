"""Abstract an storage unit."""
from zipfile import ZipFile
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

    def store_unique(self, text, _id, extension):
        """Store the file with a sha1 of its contents to avoid duplication."""
        name = _id + '.' + extension
        with self.open(name, 'wb') as file:
            file.write(text)
        if extension == 'zip':
            zip_ref = ZipFile(self.path(name), 'r')
            zip_ref.extractall(os.path.join(self.root, _id))
            zip_ref.close()

        return name
