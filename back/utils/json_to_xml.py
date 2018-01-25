from xml.dom.minidom import parseString
import dicttoxml


def learning_object_to_dicts(learning_object):
    dicts = list()
    for key, value in learning_object.items():
        temp_dict = value
        for unique_key in reversed(key.split('_')):
            temp_dict = {unique_key: temp_dict}
        dicts.append(temp_dict)
    return dicts


def merge_dicts(list_dicts):
    def deep_update(target, source):
        for k, v in source.items():
            if isinstance(v, dict):
                if not target.get(k):
                    target.update({k: {}})
                deep_update(target[k], v)
            else:
                target.update({k: v})
    result_dict = dict()
    for dict_ in list_dicts:
        deep_update(result_dict, dict_)
    return result_dict


def json_to_xml(learning_object):
    dicts = learning_object_to_dicts(learning_object)
    json_data = merge_dicts(dicts)
    del json_data['userid']
    del json_data['']
    return parseString(
        dicttoxml.dicttoxml(json_data, attr_type=False)
    ).toprettyxml()
