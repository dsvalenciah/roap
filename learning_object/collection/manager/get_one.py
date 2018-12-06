
"""
Contains utility functions to works with learning-object get one.
"""

import gettext
from manager.exceptions.learning_object import LearningObjectNotFoundError
from manager.exceptions.learning_object import LearningObjectFormatError

from manager.utils.dict_to_xml import dict_to_xml

idiomas = {
    'es': 'es_CO',
}
t = gettext.translation('get_one',
                        '../../locale',
                        languages=[idiomas['es']],
                        fallback=True)
_ = t.gettext


def get_one(db_client, learning_object_id, learning_object_format, user):
    """Get a learning object by _id."""

    learning_object = db_client.learning_objects.find_one({
        '_id': learning_object_id
    })
    _ = user.get('language')

    if not learning_object:
        raise LearningObjectNotFoundError(_('Learning Object not found.'))

    learning_object['id'] = learning_object.get('_id')

    if learning_object_format:
        format_handler = {
            'xml': lambda lo: dict_to_xml(lo.get('metadata')),
            'json': lambda lo: lo.get('metadata')
        }

        if learning_object_format not in format_handler.keys():
            raise LearningObjectFormatError(_('Unknown format.'))

        return format_handler[learning_object_format](learning_object)
    else:
        return learning_object
