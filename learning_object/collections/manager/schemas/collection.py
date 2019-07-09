from marshmallow import Schema, fields, validate


class LOCollection(Schema):
    _id = fields.UUID(required=True)
    name = fields.Str(required=True)
    sub_collections = fields.List(fields.Dict, default=[], required=False)
