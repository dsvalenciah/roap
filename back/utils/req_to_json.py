import json

import falcon


def req_to_json(req):
    try:
        raw_json = req.stream.read()
    except Exception as ex:
        # raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)
        return None

    try:
        result_json = json.loads(raw_json, encoding='utf-8')
    except ValueError:
        return None
        '''
        raise falcon.HTTPError(
            falcon.HTTP_400,
            'Malformed JSON',
            'Could not decode the request body. The '
            'JSON was incorrect.'
        )
        '''

    return result_json