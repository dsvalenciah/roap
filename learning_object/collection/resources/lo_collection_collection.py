import json
from bson.json_util import dumps
from manager.utils.req_to_dict import req_to_dict
from manager.utils.auth import Authenticate
from manager.utils.switch_language import SwitchLanguage

import falcon


@falcon.before(SwitchLanguage())
class LOCollectionCollection(object):
    def __init__(self, db_client):
        self.db_client = db_client

    @falcon.before(Authenticate())
    def on_get(self, req, resp):
        user = req.context.get('user')
        collections = get_many(
            db_client=self.db_client
        )

        resp.body = dumps(collections)

    @falcon.before(Authenticate())
    def on_post(self, req, resp):
        post_params = req_to_dict(req)
        user = req.context['user']
        _ = user.get('language')

        _id_collection = insert_one_collection(
            db_client=self.db_client,
            collection_name=post_params.get('name')
        )
        new_collection = get_one_collection(
            db_client=self.db_client, _id_collection=_id_collection)
        sub_collections_ids = list()

        for sub_collection in post_params.get('sub_collections'):
            _id_sub_collection = insert_one_sub_collection(
                db_client=self.db_client, collection_id=_id_collection, name_sub_collection=sub_collection.get('name'))
            sub_collections_ids.append(_id_sub_collection)

        new_collection.update({'sub_collection_ids': sub_collection_ids})
        modify_one_collection(
            db_client=self.db_client,
            old_collection_id=_id_collection,
            new_collection=new_collection

        )

        resp.body = dumps(
            {'id': _id_collection}
        )
        resp.status = falcon.HTTP_201
