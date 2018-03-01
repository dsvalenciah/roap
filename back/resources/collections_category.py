
"""
Contains necessary Resources to works with roap collections category
"""

from utils.req_to_dict import req_to_dict
from utils.auth import Authenticate

from bson.json_util import dumps

import falcon


class CollectionsCategory(object):
    """Deal with the whole collections of collections category."""

    def __init__(self, db):
        """Init."""
        self.db = db

    @falcon.before(Authenticate())
    def on_get(self, req, resp, user):
        """Get a single collections category."""
        if user.get('role') != 'Administrator':
            # Raise error
            pass

        if req.headers.get('AUTHORIZATION'):
            result = self.db.collections_category.find_one(
                {'_id': 'collections_category'}
            )
            if not result:
                resp.status = falcon.HTTP_404
            else:
                resp.body = dumps(result)
                resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

    @falcon.before(Authenticate())
    def on_put(self, req, resp, user):
        """Update collections category."""
        if user.get('role') != 'Administrator':
            # Raise error
            pass

        if req.headers.get('AUTHORIZATION'):
            collections_category = req_to_dict(req).get('collections_category')
            result = self.db.collections_category.update_one(
                {'_id': 'collections_category'},
                {'$set': {'collections_category': collections_category}}
            )
            if not result.acknowledged:
                resp.status = falcon.HTTP_400
            else:
                resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_401
