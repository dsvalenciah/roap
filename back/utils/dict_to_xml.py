
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


def learning_object_to_dicts(learning_object):
    """Parse learning-object from no nested dict to list of dicts."""
    dicts = list()
    for key, value in learning_object.items():
        temp_dict = value
        for unique_key in reversed(key.split('_')):
            temp_dict = {unique_key: temp_dict}
        dicts.append(temp_dict)
    return dicts


def merge_dicts(list_dicts):
    """Merge list of dicts into a single nested dict."""
    def deep_update(source, target):
        for key, value in source.items():
            if isinstance(value, dict):
                if not target.get(key):
                    target.update({key: {}})
                deep_update(value, target[key])
            else:
                target.update({key: value})
    result = dict()
    for dict_ in list_dicts:
        deep_update(dict_, result)
    return result


def no_nested_dict_to_dict(learning_object):
    """Parse learning-object from no nested dict to nested dict format."""
    dicts = learning_object_to_dicts(learning_object)
    dict_data = merge_dicts(dicts)
    del dict_data['userid']
    del dict_data['']
    return dict_data


def no_nested_dict_to_xml(learning_object):
    """Parse learning-object from no nested dict to string xml format."""
    return parse_dict_to_xml(no_nested_dict_to_dict(learning_object))
