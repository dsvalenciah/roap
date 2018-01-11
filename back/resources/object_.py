from datetime import datetime
from uuid import uuid4
import json

from schemas.object_metadata import is_valid_object
from utils.req_to_json import req_to_json

from bson.json_util import dumps

import falcon


db = None

def set_db_client(db_client):
    global db
    db = db_client

class Create:
    def on_post(self, req, resp, user_id):
        if req.headers.get("AUTHORIZATION"):
            object_ = req_to_json(req)
            valid_object, errors = is_valid_object(object_)
            if errors:
                resp.body = json.dumps({"errors": errors})
                resp.status = falcon.HTTP_400
            else:
                valid_object.update({'_id': str(uuid4().hex)})
                result = db.users.update_one(
                    {"_id": user_id},
                    {"$push": {"objects": valid_object}}
                )
                if not result.matched_count and not result.modified_count:
                    resp.status = falcon.HTTP_400
                else:
                    resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_401

class Modify:
    pass

class Query:
    pass