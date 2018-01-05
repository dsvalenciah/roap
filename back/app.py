from resources import user

import falcon

api = falcon.API()
api.add_route('/back/user/{user_id}', user.ModifierResource())
api.add_route('/back/user-create', user.CreatorResource())
api.add_route('/back/user-search', user.FinderResource())