
"""
Contains necessary Resources to works with roap collections category
"""

from utils.req_to_dict import req_to_dict

from bson.json_util import dumps

import falcon


db = None


def set_db_client(db_client):
    """Obtain db client."""
    global db
    db = db_client


class CollectionsCategory(object):
    """Deal with the whole collections of collections category."""

    def on_get(self, req, resp):
        """Get a single collections category."""
        if req.headers.get('AUTHORIZATION'):
            result = db.collections_category.find_one(
                {'_id': 'collections_category'}
            )
            if not result:
                resp.status = falcon.HTTP_404
            else:
                resp.body = dumps(result)
                resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

    def on_put(self, req, resp):
        """Update collections category."""
        if req.headers.get('AUTHORIZATION'):
            collections_category = req_to_dict(req).get('collections_category')
            result = db.collections_category.update_one(
                {'_id': 'collections_category'},
                {'$set': {'collections_category': collections_category}}
            )
            if not result.acknowledged:
                resp.status = falcon.HTTP_400
            else:
                resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_401
