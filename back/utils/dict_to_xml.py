
"""
Contains utility functions to works with learning-objects in no nested
dict format that parse it to xml content and another dict formats.
"""

from xml.etree.ElementTree import TreeBuilder, tostring
from xml.dom.minidom import parseString


lom_xml_default_attrs = {
    'xmlns:lom': 'http://ltsc.ieee.org/xsd/LOM',
    'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xsi:schemaLocation': (
        'http://ltsc.ieee.org/xsd/LOM http://ltsc.ieee.org/xsd/lomv1.0/lom.xsd'
    )
}


def parse_dict_to_xml(data):
    """Parse learning-object represented as a dict to string xml."""
    builder = deep_dict_to_xml(data)
    doc = builder.close()
    return parseString(
        tostring(doc, encoding="utf-8")
    ).toprettyxml().replace('_TP_', ':')


def deep_dict_to_xml(data, tag_name='lom', builder=None, prefix='lom_TP_'):
    """Build string xml from dict structure."""
    temp_tag_name = prefix + tag_name
    if builder is None:
        builder = TreeBuilder()
    if data is None:
        builder.start(temp_tag_name, {})
        builder.end(temp_tag_name)
    elif isinstance(data, (str, int, float, bool)):
        builder.start(temp_tag_name, {})
        builder.data(str(data))
        builder.end(temp_tag_name)
    elif isinstance(data, (list, tuple)):
        for value in data:
            deep_dict_to_xml(
                value, tag_name=tag_name, builder=builder, prefix=prefix
            )
    elif isinstance(data, dict):
        builder.start(temp_tag_name, {})
        for key, value in data.items():
            deep_dict_to_xml(
                value, tag_name=key, builder=builder, prefix=prefix
            )
        builder.end(temp_tag_name)
    else:
        raise Exception(f'I cant handle type {data}')
    return builder


def dict_to_xml(learning_object):
    """Parse learning-object from no nested dict to string xml format."""
    return parse_dict_to_xml(learning_object)
