
"""
Contains learning-object schema.
"""

from datetime import datetime

from marshmallow import Schema, fields


class LearningObject(Schema):
    """Definition for learning-object schema."""

    _id = fields.UUID(required=True)
    creator_id = fields.UUID(required=True)
    evaluator_id = fields.UUID(required=False)
    lom_schema_id = fields.UUID(required=True)
    category = fields.Str(required=True)
    created = fields.Method('get_now')
    modified = fields.Method('get_now')
    deleted = fields.Boolean(default=False)
    evaluated = fields.Boolean(default=False)
    metadata = fields.Dict(required=True)
    file_name = fields.Str(required=True)
    rating = fields.Dict(default={
        user_role: {str(i): [] for i in range(1, 6)}
        for user_role in ['expert', 'creator']
    })
    def get_now(self, obj):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

learning_object_schema = LearningObject()


def is_valid_learning_object(learning_object):
    """Check if learning-objec and his schema is matching."""
    return learning_object_schema.validate(learning_object)
