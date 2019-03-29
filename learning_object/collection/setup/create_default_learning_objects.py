
"""
Contains utility functions to populate database with a default
learning objects.
"""
import glob
import os
import gettext
from manager.insert_one import insert_one
from lxml import etree


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
        xml_tree = etree.parse(file_path)
        xml_root = xml_tree.getroot()
        technical_tag = xml_root.find('lom:technical', xml_root.nsmap)
        location_tag = technical_tag.find('lom:location', xml_root.nsmap)
        format_tag = technical_tag.find('lom:format', xml_root.nsmap)
        learning_object_id = file_path.split('/')[-1].split('.')[0]
        learning_object = db.learning_objects.find_one({
            '_id': learning_object_id
        })
        path = '../../default_files/files/'

        if os.path.isdir(os.path.join(path, f'{learning_object_id}')):
            location_tag.text = f"/learning-object-file-renderer/{learning_object_id}"
        else:
            file_name = ''
            for infile in glob.glob(os.path.join(path, f'{learning_object_id}.*')):
                file_name = infile

            location_tag.text = f"/learning-object-file-renderer/{file_name.split('/')[-1]}"

        if not learning_object:
            with open(file_path, encoding='utf-8') as file:
                learning_object_metadata = file.read()
                insert_one(
                    db_client=db,
                    learning_object_metadata=etree.tostring(xml_tree.getroot()).decode('utf-8'),
                    learning_object_id=learning_object_id,
                    learning_object_format='xml',
                    creator_id='ee6a11aee52b4e64b4a6a14d42ff49da',
                    user_language=user_language.gettext,
                    with_file=False,
                    ignore_schema=True
                )
