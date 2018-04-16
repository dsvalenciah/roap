"""Abstract an storage unit."""
import binascii
import hashlib
import os


class StorageUnit(object):
    """Abstraction for an storage unit."""

    def __init__(self, root=None):
        """Init."""
        if root is None:
            self.root = os.getenv('FILE_STORAGE')
        else:
            self.root = root

    def open(self, name, mode='r'):
        """Open a file from the storage unit."""
        return open(self.path(name), mode)

    def path(self, name):
        """Create a path relative to the storage units root."""
        return os.path.join(self.root, name)

    def store_unique(self, text, extension):
        """Store the file with a sha1 of its contents to avoid duplication."""
        sha1 = hashlib.pbkdf2_hmac('sha1', text.encode(), b'', 100000)
        name = binascii.hexlify(sha1).decode() + extension
        created = os.path.isfile(self.path(name))
        if not created:
            with self.open(name, 'a+') as file:
                file.write(text)

        return name, created
