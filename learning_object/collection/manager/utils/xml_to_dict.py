
"""
Contains utility functions to work with learning-objects as a xml based
on lom standard that parse from xml content to dict format.
"""

import xmltodict


def delete_n_first_characters_from_keys(source, target, n=4):
    """Delete n first characters from all keys in nested dict."""
    for key, value in source.items():
        new_key = key[n:]
        if isinstance(value, dict):
            if not target.get(new_key):
                target.update({new_key: {}})
            delete_n_first_characters_from_keys(value, target[new_key], n)
        else:
            target.update({new_key: value})


def xml_to_dict(xml_content):
    """Parse learning-object in xml string format to dict."""
    dict_content = xmltodict.parse(xml_content, encoding='utf-8')
    new_dict_content = dict()
    # Delete first 4 characters that represents 'lom:'
    delete_n_first_characters_from_keys(dict_content, new_dict_content)
    return new_dict_content.get('lom')
