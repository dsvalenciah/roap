
"""
Contains utility functions to populate database with a default
learning objects.
"""
import glob
import pkgutil
import os
import encodings

from exceptions.learning_object import (
    LearningObjectSchemaError, LearningObjectMetadataSchemaError
)

from utils.learning_object import LearningObject
from utils.xml_to_dict import xml_to_dict


def all_encodings():
    modnames = set(
        [modname for importer, modname, ispkg in pkgutil.walk_packages(
            path=[os.path.dirname(encodings.__file__)], prefix='')])
    aliases = set(encodings.aliases.aliases.values())
    return modnames.union(aliases)


def learning_object_populate(db):
    """Populate database with default learning objects."""
    encodings = all_encodings()
    learning_object_manager = LearningObject(db)
    list_files_path = glob.glob("config/data/learning_objects_xml/*.xml")
    for file_path in list_files_path:
        _id, _ = file_path.split('/')[-1].split('.')
        learning_object = db.learning_objects.find_one({'_id': _id})
        if not learning_object:
            learning_object_metadata = None
            for enc in encodings:
                try:
                    with open(file_path, encoding=enc) as file:
                        learning_object_metadata = xml_to_dict(
                            file.read()
                        )
                except Exception as e:
                    pass
            try:
                learning_object_manager.insert_one(
                    learning_object_metadata,
                    user={
                        'deleted': False,
                        'role': 'administrator',
                        '_id': 'ee6a11aee52b4e64b4a6a14d42ff49da'
                    },
                    ignore_schema=True
                )
            except LearningObjectMetadataSchemaError as e:
                print(e)
