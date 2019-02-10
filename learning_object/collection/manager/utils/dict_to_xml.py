
"""
Contains utility functions to works with learning-objects in no nested
dict format that parse it to xml content and another dict formats.
"""

import xmltodict


lom_xml_default_attrs = {
    '@xmlns:lom': 'http://ltsc.ieee.org/xsd/LOM',
    '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    '@xsi:schemaLocation': (
        'http://ltsc.ieee.org/xsd/LOM http://ltsc.ieee.org/xsd/lomv1.0/lom.xsd'
    )
}


def add_lom_prefix_to_keys(source, target):
    for key, value in source.items():
        new_key = f'lom:{key}'
        if isinstance(value, dict):
            if not target.get(new_key):
                target.update({new_key: {}})
            add_lom_prefix_to_keys(value, target[new_key])
        else:
            target.update({new_key: value})


def dict_to_xml(learning_object):
    """Parse learning-object from no nested dict to string xml format."""
    new_learning_object_content = dict()
    add_lom_prefix_to_keys(learning_object, new_learning_object_content)
    new_learning_object_content = {
        'lom:lom': {
            **lom_xml_default_attrs,
            **new_learning_object_content
        }
    }
    full_parsed_xml = xmltodict.unparse(
        new_learning_object_content,
        encoding='utf-8',
        pretty=True,
        full_document=False
    )
    return learning_object, full_parsed_xml
