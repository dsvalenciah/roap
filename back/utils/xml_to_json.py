from xml.etree import ElementTree as ET
import re
import json

def delete_trash(trash, string, replace):
    new_string = re.sub(trash, replace, string)
    return new_string


def parse_xml_to_json(xml):
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
            str_xml = delete_trash(trash, string + element.tag, '')

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


xml = ET.ElementTree(file='my_xml.xml').getroot()
parsed = parse_xml_to_json(xml)

print(parsed)
