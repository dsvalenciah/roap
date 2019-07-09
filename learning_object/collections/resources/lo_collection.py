import json
import falcon
from manager import SwitchLanguage, CollectionNotFoundError, Authenticate, get_one_collection, modify_one_collection, req_to_dict, SubCollectionUndeleteError
from bson.json_util import dumps


@falcon.before(SwitchLanguage())
class LOCollection(object):
    def __init__(self, db_client):
        self.db_client = db_client

    @falcon.before(Authenticate())
    def on_get(self, req, resp, _id):
        try:
            user = req.context.get('user')
            collection = get_one_collection(
                db_client=self.db_client,
                collection_id=_id,
                user=user
            )
            collection['id'] = collection['_id']
            resp.body = dumps(collection)
        except CollectionNotFoundError as e:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)}
            )

    @falcon.before(Authenticate())
    def on_put(self, req, resp, _id):
        try:
            new_collection = req_to_dict(req)
            print(new_collection)
            auth_user = req.context.get('user')
            modify_one_collection(
                db_client=self.db_client,
                collection_id=_id,
                new_collection=new_collection,
                user=auth_user,
            )
            resp.body = dumps({'data': new_collection})
        except CollectionNotFoundError as e:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
        except SubCollectionUndeleteError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = dumps(
                {'message': json.dumps(e.args[0], ensure_ascii=False)})
