import json

from resources import user
from resources import object_
from resources import object_metadata

from config.object_metadata import learning_object_schema_populate

import falcon

learning_object_schema_populate()

api = falcon.API()

api.add_route('/back/obj-meta', object_metadata.Query())
api.add_route('/back/obj-meta-create', object_metadata.Create())
api.add_route('/back/obj-meta/{field_id}', object_metadata.Modify())

api.add_route('/back/obj', object_.Query())
api.add_route('/back/obj-create/{user_id}', object_.Create())
api.add_route('/back/obj/{user_id}/{object_id}', object_.Modify())

api.add_route('/back/user', user.Query())
api.add_route('/back/user-create', user.Create())
api.add_route('/back/user/{user_id}', user.Modify())