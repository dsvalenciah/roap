"""
Contains utility functions to populate database with a default
learning objects.
"""
import glob
import gettext
from manager.insert_one import insert_one


def create_default_learning_objects(db):
    """Populate database with default learning objects."""
    # TODO: fix category
    list_files_path = glob.glob("setup/default_learning_objects_xml/*.xml")
    user_language = gettext.translation(
        'collection', '/code/locale', languages=['en_US'])
    db.learning_objects.drop_indexes()

    db.learning_objects.create_index(
        [
            ("$**", "text"),
        ],
        language_override='es'
    )

    for file_path in list_files_path:
        learning_object_id = file_path.split('/')[-1].split('.')[0]
        learning_object = db.learning_objects.find_one({
            '_id': learning_object_id
        })
        if not learning_object:
            with open(file_path, encoding='utf-8') as file:
                learning_object_metadata = file.read()
                insert_one(
                    db_client=db,
                    learning_object_metadata=learning_object_metadata,
                    learning_object_id=learning_object_id,
                    learning_object_format='xml',
                    creator_id='ee6a11aee52b4e64b4a6a14d42ff49da',
                    user_language=user_language.gettext,
                    with_file=False,
                    ignore_schema=True,
                    status='accepted'
                )
