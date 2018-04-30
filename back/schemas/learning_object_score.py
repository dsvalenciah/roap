
"""
Contains user-rating schema.
"""

from marshmallow import Schema, fields, validate


class LearningObjectRating(Schema):
    """Definition for learning-object schema."""
    # TODO: use this.
    learning_object_id = fields.UUID(required=True)
    user_id = fields.UUID(required=True)
    rating = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=5)
    )
    created = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    user_role = fields.Str(required=True, validate=validate.OneOf(
        ['administrator', 'expert', 'creator', 'unknown']
    ))
