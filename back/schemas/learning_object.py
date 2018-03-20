
"""
Contains learning-object schema.
"""

from marshmallow import Schema, fields, validate


class LearningObject(Schema):
    """Definition for learning-object schema."""

    _id = fields.UUID(required=True)
    user_id = fields.UUID(required=True)
    lom_schema_id = fields.UUID(required=True)
    category = fields.Str(required=True)
    created = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    modified = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    deleted = fields.Boolean(required=True)
    evaluated = fields.Boolean(required=True)
    metadata = fields.Dict(required=True)
    files_path = fields.List(fields.Str, required=True)

learning_object_schema = LearningObject()


def is_valid_learning_object(learning_object):
    """Check if learning-objec and his schema is matching."""
    return learning_object_schema.validate(learning_object)
