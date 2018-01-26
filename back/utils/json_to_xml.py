from xml.etree.ElementTree import TreeBuilder, tostring
from xml.dom.minidom import parseString


lom_xml_default_attrs = {
    'xmlns:lom': 'http://ltsc.ieee.org/xsd/LOM',
    'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xsi:schemaLocation': 'http://ltsc.ieee.org/xsd/LOM http://ltsc.ieee.org/xsd/lomv1.0/lom.xsd'
}


def parse_json_to_xml(json_data):
    builder = deep_json_to_xml(json_data)
    doc = builder.close()
    return parseString(
        tostring(doc, encoding="utf-8")
    ).toprettyxml().replace('_TP_', ':')


def deep_json_to_xml(data, tag_name='lom', builder=None, prefix='lom_TP_'):
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
            deep_json_to_xml(
                value, tag_name=tag_name, builder=builder, prefix=prefix
            )
    elif isinstance(data, dict):
        builder.start(temp_tag_name, {})
        for key, value in data.items():
            deep_json_to_xml(
                value, tag_name=key, builder=builder, prefix=prefix
            )
        builder.end(temp_tag_name)
    else:
        raise Exception(f'I cant handle type {data}')
    return builder


def learning_object_to_dicts(learning_object):
    dicts = list()
    for key, value in learning_object.items():
        temp_dict = value
        for unique_key in reversed(key.split('_')):
            temp_dict = {unique_key: temp_dict}
        dicts.append(temp_dict)
    return dicts


def merge_dicts(list_dicts):
    def deep_update(source, target):
        for k, v in source.items():
            if isinstance(v, dict):
                if not target.get(k):
                    target.update({k: {}})
                deep_update(v, target[k])
            else:
                target.update({k: v})
    result_dict = dict()
    for dict_ in list_dicts:
        deep_update(dict_, result_dict)
    return result_dict


def roapjson_to_xml(learning_object):
    dicts = learning_object_to_dicts(learning_object)
    json_data = merge_dicts(dicts)
    del json_data['userid']
    del json_data['']
    return parse_json_to_xml(json_data)


def roapjson_to_json(learning_object):
    dicts = learning_object_to_dicts(learning_object)
    json_data = merge_dicts(dicts)
    del json_data['userid']
    del json_data['']
    return json_data
