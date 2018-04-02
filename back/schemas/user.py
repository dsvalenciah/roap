
"""
Contains user schema.
"""

from marshmallow import Schema, fields, validate


class User(Schema):
    """Definition for user schema."""

    # TODO: add keywords and notifications?

    _id = fields.UUID(required=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    email = fields.Str(
        required=True,
        validate=validate.Email(error='Not a valid email address')
    )
    role = fields.Str(required=True, validate=validate.OneOf(
        ['administrator', 'expert', 'creator', 'unknown']
    ))
    requested_role = fields.Str(required=True, validate=validate.OneOf(
        ['administrator', 'expert', 'creator', 'unknown']
    ))
    created = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    modified = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    deleted = fields.Boolean(required=True)
    last_activity = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    validated = fields.Boolean(required=True)

user_schema = User()


def is_valid_user(user):
    """Check if user and his schema is matching."""
    return user_schema.validate(user)
