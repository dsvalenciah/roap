
"""
Contains utility functions to work with learning-objects as a xml based
on lom standard that parse from xml content to dict format.
"""

from xml.etree import ElementTree
import re
import json


def delete_trash(trash, string, replace):
    """Replace a string contained in a string by another string."""
    return re.sub(trash, replace, string)


def parse_xml_to_dict(xml):
    """Parse xml content to dumped no nested dict."""
    parents = []
    trash = '{http://ltsc.ieee.org/xsd/LOM}'
    my_dict = dict()

    for element in xml.iter():
        string = ''
        continue_for = False
        while len(element) >= 1:
            parents.append(element)
            continue_for = True
            break
        if continue_for:
            continue
        else:
            for x in parents:
                string += x.tag + '_'
            last_element = parents[len(parents) - 1]
            if last_element[len(last_element) - 1] == element:
                parents.pop()
                for x in parents:
                    if x[len(x) - 1] == last_element:
                        parents.remove(x)
            str_xml = delete_trash(trash, string + element.tag, '')[4:]

            if str_xml in my_dict:
                if isinstance(my_dict[str_xml], list):
                    my_dict[str_xml].append(element.text)
                else:
                    my_dict[str_xml] = [my_dict[str_xml]]
                    my_dict[str_xml].append(element.text)
            else:
                my_dict[str_xml] = element.text

    my_dict = json.dumps(my_dict)
    return my_dict


def xml_to_dict(xml_content):
    """
    Parse learning-object in xml string format to no nested dict.

    Nested dict is represented with keys delimited with underscores.
    """
    xml = ElementTree.ElementTree(
        ElementTree.fromstring(xml_content)
    ).getroot()
    return json.loads(parse_xml_to_dict(xml))
