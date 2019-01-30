
"""
Contains utility functions to work with learning-objects as a xml based
on lom standard that parse from xml content to dict format.
"""

import xmltodict


def remove_lom_prefix_to_keys(source, target):
    for key, value in source.items():
        new_key = key[4:]
        if isinstance(value, dict):
            if not target.get(new_key):
                target.update({new_key: {}})
            remove_lom_prefix_to_keys(value, target[new_key])
        else:
            target.update({new_key: value})


def xml_to_dict(xml_content):
    """Parse learning-object in xml string format to dict."""
    dict_content = xmltodict.parse(xml_content, encoding='utf-8')
    new_dict_content = dict()
    remove_lom_prefix_to_keys(dict_content, new_dict_content)
    full_parsed_dict = new_dict_content.get('lom')
    tags_to_clean = ["ns:lom", "ns:xsi", ":schemaLocation"]
    for tag_to_clean in tags_to_clean:
        full_parsed_dict.pop(tag_to_clean, None)
    return full_parsed_dict, xml_content
