import json
from bson.json_util import dumps

from manager import(
    req_to_dict, Authenticate, SwitchLanguage,
    get_many_sub_collections, 
    CollectionNotFoundError, UserPermissionError
)

import falcon


@falcon.before(SwitchLanguage())
class LOSubCollectionCollection(object):
    def __init__(self, db_client):
        self.db_client = db_client

    def on_get(self, req, resp):
        query_params = {
            k: json.loads(v)
            for k, v in req.params.items()
        }
        try:
            filter_ = query_params.get('filter', {})
            range_ = query_params.get('range', [0, 9])
            sorted_ = query_params.get('sort', ['lo_quantity', 'desc'])
            sub_collections, total_count = get_many_sub_collections(
                db_client=self.db_client,
                filter_=filter_,
                range_=range_,
                sorted_=sorted_
            )
            for sub_collection in sub_collections:
                sub_collection['id'] = sub_collection['_id']
            resp.body = dumps(sub_collections)
            len_sub_collections = len(sub_collections)
            resp.content_range = (
                range_[0],
                len_sub_collections - range_[0],
                total_count,
                'sub_collections'
            )
        except ValueError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})