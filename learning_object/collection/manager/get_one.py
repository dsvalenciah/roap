
"""
Contains utility functions to works with learning-object get one.
"""

from manager.exceptions.learning_object import LearningObjectNotFoundError
from manager.exceptions.learning_object import LearningObjectFormatError

from manager.utils.dict_to_xml import dict_to_xml

def get_one(
        db_client, learning_object_id, learning_object_format,
        only_metadata=True):
    """Get a learning object by _id."""

    learning_object = db_client.learning_objects.find_one({
        '_id': learning_object_id
    })

    if not learning_object:
        raise LearningObjectNotFoundError(['Learning Object _id not found.'])

    if only_metadata:
        format_handler = {
            'xml': lambda lo: dict_to_xml(lo.get('metadata')),
            'json': lambda lo: lo.get('metadata')
        }

        if learning_object_format not in format_handler.keys():
            raise LearningObjectFormatError(['Unknown format.'])

        return format_handler[learning_object_format](learning_object)
    else:
        return learning_object