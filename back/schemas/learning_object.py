
"""
Contains learning-object schema.
"""

from marshmallow import Schema, fields, validate


class LearningObject(Schema):
    """Definition for learning-object schema."""

    _id = fields.UUID(required=True)
    user_uid = fields.UUID(required=True)
    evaluator_uid = fields.UUID(required=False)
    created = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    modified = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    schema = fields.Dict(required=True)
    metadata = fields.Dict(required=True)
    state = fields.Str(required=True, validate=validate.OneOf(
        ['active', 'unevaluated', 'inactive']
    ))
    user_ranking = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=5)
    )
    evaluator_ranking = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=5)
    )
    files = fields.List(fields.Str, required=True)

learning_object_schema = LearningObject()


def is_valid_learning_object(learning_object):
    """Check if learning-objec and his schema is matching."""
    return learning_object_schema.validate(learning_object)
