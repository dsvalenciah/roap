
"""
Contains utility functions to populate database with a default
learning objects.
"""
import glob
import pkgutil
import os
import encodings
from random import randint

from exceptions.learning_object import (
    LearningObjectSchemaError, LearningObjectMetadataSchemaError
)

from utils.learning_object import LearningObject
from utils.learning_object import LearningObjectScore
from utils.xml_to_dict import xml_to_dict


def all_encodings():
    modnames = set(
        [modname for importer, modname, ispkg in pkgutil.walk_packages(
            path=[os.path.dirname(encodings.__file__)], prefix='')])
    aliases = set(encodings.aliases.aliases.values())
    return modnames.union(aliases)


def learning_object_populate(db):
    """Populate database with default learning objects."""
    # TODO: fix category
    encodings = all_encodings()
    learning_object_manager = LearningObject(db)
    learning_object_score_manager = LearningObjectScore(db)
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
                role = [
                    'administrator', 'expert', 'creator'
                ][randint(0, 2)]
                learning_object_manager.insert_one(
                    {
                        'lom': learning_object_metadata,
                        'category': [
                            "Educacion", "Medicina", "Fisica"
                        ][randint(0, 2)]
                    },
                    user={
                        'deleted': False,
                        'role': role,
                        '_id': 'ee6a11aee52b4e64b4a6a14d42ff49da'
                    },
                    ignore_schema=True,
                    _id=_id
                )
                learning_object_score_manager.insert_one(
                    _id,
                    {
                        'deleted': False,
                        'role': role,
                        '_id': 'ee6a11aee52b4e64b4a6a14d42ff49da'
                    },
                    randint(1, 5)
                )
            except LearningObjectMetadataSchemaError as e:
                print(e)
