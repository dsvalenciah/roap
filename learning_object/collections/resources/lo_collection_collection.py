import json
from bson.json_util import dumps

from manager import(
    insert_one_sub_collection, req_to_dict, Authenticate, SwitchLanguage,
    get_many_collections, insert_one_collection, get_one_collection, modify_one_collection,
    CollectionNotFoundError, UserPermissionError, CollectionSchemaError, SubCollectionSchemaError
)

import falcon


@falcon.before(SwitchLanguage())
class LOCollectionCollection(object):
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
            collections, total_count = get_many_collections(
                db_client=self.db_client,
                filter_=filter_,
                range_=range_,
                sorted_=sorted_
            )
            for collection in collections:
                collection['id'] = collection['_id']
            resp.body = dumps(collections)
            len_collections = len(collections)
            resp.content_range = (
                range_[0],
                len_collections - range_[0],
                total_count,
                'collections'
            )
        except ValueError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})

    @falcon.before(Authenticate())
    def on_post(self, req, resp):
        post_params = req_to_dict(req)
        user = req.context['user']
        _ = user.get('language')

        try:
            _id_collection = insert_one_collection(
                db_client=self.db_client,
                collection_name=post_params.get('name'), user=user
            )
            new_collection = get_one_collection(
                db_client=self.db_client, collection_id=_id_collection, user=user)

            sub_collection_ids = list()

            for sub_collection in post_params.get('sub_collections'):
                _id_sub_collection = insert_one_sub_collection(
                    db_client=self.db_client, collection_id=_id_collection, name_sub_collection=sub_collection.get('name'), user=user)
                sub_collection_ids.append(_id_sub_collection)

            new_collection.update({'sub_collection_ids': sub_collection_ids})

            modify_one_collection(
                db_client=self.db_client,
                collection_id=_id_collection,
                new_collection=new_collection,
                user=user
            )

            resp.body = dumps(
                {'id': _id_collection}
            )
            resp.status = falcon.HTTP_201
        except UserPermissionError as e:
            resp.status = falcon.HTTP_UNAUTHORIZED
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)}
            )
        except CollectionSchemaError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)}
            )
        except CollectionNotFoundError as e:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except SubCollectionSchemaError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)}
            )
