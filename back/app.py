import json

from resources import user
from resources import metadata

from config.learning_object import learning_object_schema_populate

import falcon

learning_object_schema_populate()

api = falcon.API()

api.add_route('/back/learn-obj-schema/{field_id}', metadata.ModifierResource())
api.add_route('/back/learn-obj-schema-create', metadata.CreatorResource())
api.add_route('/back/learn-obj-schema-search', metadata.FinderResource())
api.add_route(
    '/back/validate-learning-object', metadata.ValidateLearningObject()
)

api.add_route('/back/user/{user_id}', user.ModifierResource())
api.add_route('/back/user-create', user.CreatorResource())
api.add_route('/back/user-search', user.FinderResource())