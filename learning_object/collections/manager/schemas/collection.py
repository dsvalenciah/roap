from marshmallow import Schema, fields, validate

class SubCollection(Schema):
    _id = fields.UUID(required=True)
    name = fields.Str(required=True)
    collection_id = fields.UUID(required=True)

class LOCollection(Schema):
    _id = fields.UUID(required=True)
    name = fields.Str(required=True)
    sub_collection_ids = fields.List(fields.UUID(), default=[], required=False)