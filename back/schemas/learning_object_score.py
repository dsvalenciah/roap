
"""
Contains user-score schema.
"""

from marshmallow import Schema, fields, validate


class LearningObjectScore(Schema):
    """Definition for learning-object schema."""

    learning_object_id = fields.UUID(required=True)
    user_id = fields.UUID(required=True)
    score = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=5)
    )
    created = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    user_role = fields.Str(required=True, validate=validate.OneOf(
        ['administrator', 'expert', 'creator', 'unknown']
    ))
