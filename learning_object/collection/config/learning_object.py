
"""
Contains utility functions to populate database with a default
learning objects.
"""
import glob

from manager.insert_one import insert_one


def learning_object_populate(db):
    """Populate database with default learning objects."""
    # TODO: fix category
    list_files_path = glob.glob("config/data/learning_object_xml/*.xml")

    db.learning_objects.drop_indexes()

    db.learning_objects.create_index(
        [
            ("metadata.general.description", "text"),
            ("metadata.general.title", "text"),
            # ("metadata.general.keyword", "text")
        ],
        language_override='es'
    )

    # TODO: manage more languages than spanish.

    for file_path in list_files_path:
        learning_object_id = file_path.split('/')[-1].split('.')[0]
        learning_object = db.learning_objects.find_one({
            '_id': learning_object_id
        })
        if not learning_object:
            learning_object_metadata = None
            try:
                with open(file_path, encoding='utf-8') as file:
                    learning_object_metadata = file.read()
            except Exception as e:
                raise ValueError(e)
            if learning_object_metadata:
                insert_one(
                    db_client=db,
                    learning_object_metadata=learning_object_metadata,
                    learning_object_id=learning_object_id,
                    learning_object_format='xml',
                    creator_id='ee6a11aee52b4e64b4a6a14d42ff49da',
                    with_file=False,
                    ignore_schema=True
                )
