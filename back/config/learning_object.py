
"""
Contains utility functions to populate database with a default
learning objects.
"""
import glob
from random import randint

from exceptions.learning_object import (
    LearningObjectSchemaError, LearningObjectMetadataSchemaError
)

from utils.storage import StorageUnit
from utils.learning_object import LearningObject
from utils.learning_object import LearningObjectRating
from utils.xml_to_dict import xml_to_dict


def learning_object_populate(db):
    """Populate database with default learning objects."""
    # TODO: fix category
    storage = StorageUnit()
    learning_object_manager = LearningObject(db)
    learning_object_rating_manager = LearningObjectRating(db)
    list_files_path = glob.glob("config/data/learning_objects_xml/*.xml")

    db.learning_objects.drop_indexes()

    db.learning_objects.create_index(
        [
            ("metadata.general.description", "text"),
            ("metadata.general.title", "text"),
            ("metadata.general.keyword", "text")
        ],
        language_override='es'
    )

    # TODO: manage more languages than espanish.

    for file_path in list_files_path:
        _id, _ = file_path.split('/')[-1].split('.')
        learning_object = db.learning_objects.find_one({'_id': _id})
        learing_object_file_path = glob.glob(
            f"config/data/files/{_id}.*"
        )[0]
        if not learning_object:
            learning_object_metadata = None
            try:
                with open(file_path, encoding='utf-8') as file:
                    learning_object_metadata = xml_to_dict(
                        file.read()
                    )
            except Exception as e:
                raise ValueError(e)
            if learning_object_metadata:
                try:
                    role = [
                        'administrator', 'expert', 'creator'
                    ][randint(0, 2)]
                    learning_object_manager.insert_one(
                        learning_object={
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
                        file={
                            'file_extension': (
                                learing_object_file_path.split('.')[-1]
                            ),
                            'file_content': open(
                                learing_object_file_path, "rb"
                            ).read()
                        },
                        ignore_schema=True,
                        _id=_id
                    )
                    learning_object_rating_manager.insert_one(
                        _id,
                        {
                            'deleted': False,
                            'role': role,
                            '_id': 'ee6a11aee52b4e64b4a6a14d42ff49da'
                        },
                        randint(1, 5)
                    )
                except LearningObjectMetadataSchemaError as e:
                    raise ValueError(e.args[0])
