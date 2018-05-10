
"""
Contains learning-object schema.
"""

from datetime import datetime

from marshmallow import Schema, fields


class LearningObject(Schema):
    """Definition for learning-object schema."""

    _id = fields.UUID(required=True)
    user_id = fields.UUID(required=True)
    lom_schema_id = fields.UUID(required=True)
    category = fields.Str(required=True)
    created = fields.DateTime(
        default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        format='%Y-%m-%d %H:%M:%S'
    )
    modified = fields.DateTime(
        default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        format='%Y-%m-%d %H:%M:%S'
    )
    deleted = fields.Boolean(default=False)
    evaluated = fields.Boolean(default=False)
    metadata = fields.Dict(required=True)
    file_name = fields.Str(required=True)
    rating = fields.Dict(default={
        user_role: {str(i): [] for i in range(1, 6)}
        for user_role in ['expert', 'creator']
    })

learning_object_schema = LearningObject()


def is_valid_learning_object(learning_object):
    """Check if learning-objec and his schema is matching."""
    return learning_object_schema.validate(learning_object)
