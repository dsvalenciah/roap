import json
import os

from pymongo import MongoClient
from bson.json_util import dumps

from marshmallow import fields, Schema, validate
import marshmallow


client = MongoClient(os.getenv('DB_HOST'), 27017)
db = client.roap

validators_list = {
    "containsonly": validate.ContainsOnly,  # (choices, labels=None, error=None),
    "email": validate.Email,  # (error=None),
    "equal": validate.Equal,  # (comparable, error=None),
    "length": validate.Length,  # (min=None, max=None, error=None, equal=None),
    "noneof": validate.NoneOf,  # (iterable, error=None),
    "oneof": validate.OneOf,  # (choices, labels=None, error=None),
    "range": validate.Range,  # (min=None, max=None, error=None),
    "regexp": validate.Regexp,  # (regex, flags=0, error=None)
    "url": validate.URL,  # (relative=False, error=None, schemes=None, require_tld=True)
}

fields_list = {
    "field": fields.Field,  # (default=<marshmallow.missing>, attribute=None, load_from=None, dump_to=None, error=None, validate=None, required=False, allow_none=None, load_only=False, dump_only=False, missing=<marshmallow.missing>, error_messages=None, **metadata)
    "raw": fields.Raw,  # (default=<marshmallow.missing>, attribute=None, load_from=None, dump_to=None, error=None, validate=None, required=False, allow_none=None, load_only=False, dump_only=False, missing=<marshmallow.missing>, error_messages=None, **metadata)
    "dict": fields.Dict,  # (values=None, keys=None, **kwargs)
    "list": fields.List,  # (cls_or_instance, **kwargs)
    "string": fields.String,  # (default=<marshmallow.missing>, attribute=None, load_from=None, dump_to=None, error=None, validate=None, required=False, allow_none=None, load_only=False, dump_only=False, missing=<marshmallow.missing>, error_messages=None, **metadata)
    "uuid": fields.UUID,  # (default=<marshmallow.missing>, attribute=None, load_from=None, dump_to=None, error=None, validate=None, required=False, allow_none=None, load_only=False, dump_only=False, missing=<marshmallow.missing>, error_messages=None, **metadata)
    "number": fields.Number,  # (as_string=False, **kwargs)
    "integer": fields.Integer,  # (strict=False, **kwargs)
    "decimal": fields.Decimal,  # (places=None, rounding=None, allow_nan=False, as_string=False, **kwargs)
    "boolean": fields.Boolean,  # (truthy=None, falsy=None, **kwargs)
    "float": fields.Float,  # (as_string=False, **kwargs)
    "datetime": fields.DateTime,  # (format=None, **kwargs)
    "time": fields.Time,  # (default=<marshmallow.missing>, attribute=None, load_from=None, dump_to=None, error=None, validate=None, required=False, allow_none=None, load_only=False, dump_only=False, missing=<marshmallow.missing>, error_messages=None, **metadata)
    "date": fields.Date,  # (default=<marshmallow.missing>, attribute=None, load_from=None, dump_to=None, error=None, validate=None, required=False, allow_none=None, load_only=False, dump_only=False, missing=<marshmallow.missing>, error_messages=None, **metadata)
    "url": fields.Url,  # (relative=False, schemes=None, **kwargs)
    "email": fields.Email,  # (*args, **kwargs)
}

class Validate(Schema):
    kind = fields.Str(required=True, validate=validate.OneOf(
        choices=validators_list.keys()
    ))
    params = fields.Dict(required=True)

class FieldParams(Schema):
    validate = fields.Nested(Validate, required=False)
    required = fields.Boolean(required=False)

class Field(Schema):
    _id = fields.Str(required=True)
    name = fields.Str(required=True)
    kind = fields.Str(required=True, validate=validate.OneOf(
        choices=fields_list.keys()
    ))
    params = fields.Nested(FieldParams, required=True)

def dict_to_schema(fields):
    data, errors = Field(many=True).load(fields)
    if errors:
        return errors
    else:
        parsed_fields = dict()
        for field in fields:
            if field.get("params").get("validate"):
                field["params"]["validate"] = (validators_list.get(
                    field.get("params").get("validate").get("kind")
                )(
                    **field.get("params").get("validate").get("params")
                ))

            parsed_fields.update({
                field.get("name"): fields_list.get(
                    field.get("kind")
                )(**field.get("params"))
            })

        return type('MySchema', (marshmallow.Schema,), parsed_fields)()

def is_valid_schema_field(field):
    return Field().load(field)

def is_valid_learning_object(data):
    schema_fields = json.loads(dumps(db.learning_object_metadadta.find()))
    generic_schema = dict_to_schema(schema_fields)
    if len(data) > len(schema_fields):
        return "Invalid number of attribiutes"
    if not isinstance(generic_schema, dict):
        return generic_schema.load(data)[1]
    else:
        return generic_schema
