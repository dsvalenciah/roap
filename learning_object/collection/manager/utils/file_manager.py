"""Abstract an storage unit."""
from zipfile import ZipFile
from glob import glob
from uuid import uuid4
import shutil
import base64
import os

from manager.exceptions.learning_object import LearningObjectFile

supported_mimetypes = [
  "application/msword",
  "application/msword",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.template",
  "application/vnd.ms-word.document.macroEnabled.12",
  "application/vnd.ms-word.template.macroEnabled.12",
  "application/vnd.ms-excel",
  "application/vnd.ms-excel",
  "application/vnd.ms-excel",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.template",
  "application/vnd.ms-excel.sheet.macroEnabled.12",
  "application/vnd.ms-excel.template.macroEnabled.12",
  "application/vnd.ms-excel.addin.macroEnabled.12",
  "application/vnd.ms-excel.sheet.binary.macroEnabled.12",
  "application/vnd.ms-powerpoint",
  "application/vnd.ms-powerpoint",
  "application/vnd.ms-powerpoint",
  "application/vnd.ms-powerpoint",
  "application/vnd.openxmlformats-officedocument.presentationml.presentation",
  "application/vnd.openxmlformats-officedocument.presentationml.template",
  "application/vnd.openxmlformats-officedocument.presentationml.slideshow",
  "application/vnd.ms-powerpoint.addin.macroEnabled.12",
  "application/vnd.ms-powerpoint.presentation.macroEnabled.12",
  "application/vnd.ms-powerpoint.template.macroEnabled.12",
  "application/vnd.ms-powerpoint.slideshow.macroEnabled.12",
  "video/webm",
  "video/mp4",
  "video/ogg",
  "audio/webm",
  "audio/ogg",
  "audio/mpeg",
  "audio/wave",
  "audio/wav",
  "audio/x-wav",
  "audio/x-pn-wav",
  "audio/flac",
  "audio/x-flac",
  "image/gif",
  "image/png",
  "image/jpeg",
  "image/bmp",
  "image/webp",
  "image/vnd.microsoft.icon",
  "application/zip",
  "application/pdf",
]


class StorageUnit(object):
    """Abstraction for an storage unit."""

    def __init__(self, exceptions_language_handler, root=None):
        """Init."""
        self._ = exceptions_language_handler
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

    def find_in_folder(self, folder_path, file_name):
        files_path = list(glob(folder_path + '/*.*'))
        for file_path in files_path:
            if file_name in file_path:
                return True
        return False

    def delete_folder(self, folder_path):
        shutil.rmtree(folder_path)

    def delete_file(self, file_name):
        os.remove(os.path.join(self.root, file_name))

    def store(self, base64_file_content, file_metadata):
        """Store the file with a sha1 of its contents to avoid duplication."""

        if len(file_metadata.get('name', '.').split('.')) < 2:
            raise LearningObjectFile(self._('Incorrect file name.'))
        if file_metadata.get('mime_type') not in supported_mimetypes:
            raise LearningObjectFile(self._('Not supported file mimetype.'))

        file_extension = file_metadata.get('extension')
        file_name = file_metadata.get('_id') + file_extension
        file_id = file_metadata.get('_id')
        with self.open(file_name, mode='wb') as file:
            file.write(base64.decodebytes(base64_file_content.encode("ascii")))

        if file_extension == '.zip':
            folder_path = os.path.join(self.root, file_id)
            with self.open(file_name, mode='rb') as file:
                zip_ref = ZipFile(file)
                zip_ref.extractall(folder_path)
            # Validate index.html in zipfile
            if not self.find_in_folder(folder_path, 'index.html'):
                self.delete_file(file_name)
                self.delete_folder(folder_path)
                raise LearningObjectFile(self._('Folder without index.html.'))
