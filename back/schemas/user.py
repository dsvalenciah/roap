
"""
Contains user schema.
"""

from marshmallow import Schema, fields, validate


class User(Schema):
    """Definition for user schema."""

    _id = fields.Str(required=True)
    name = fields.Str(required=True)
    email = fields.Str(
        required=True,
        validate=validate.Email(error='Not a valid email address')
    )
    role = fields.Str(required=True, validate=validate.OneOf(
        ['administrator', 'expert', 'creator', 'external']
    ))
    created = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    modified = fields.Str(required=False)

user_schema = User()


def is_valid_user(user):
    """Check if user and his schema is matching."""
    return user_schema.load(user)
