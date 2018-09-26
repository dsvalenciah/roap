
"""
Contains learning-object schema.
"""

from datetime import datetime

from marshmallow import Schema, fields


class FileMetadata(Schema):
    _id = fields.UUID(required=True)
    extension = fields.Str(required=True)
    name = fields.Str(required=True)
    mime_type = fields.Str(required=True)
    size = fields.Integer(required=True)
    last_modified = fields.Str(required=True)

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
    file_metadata = fields.Nested(FileMetadata, required=True)
    rating = fields.Dict(default={
        user_role: {str(i): [] for i in range(1, 6)}
        for user_role in ['expert', 'creator']
    })
    def get_now(self, obj):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
