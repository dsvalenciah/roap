
"""
Contains user schema.
"""

from datetime import datetime
from uuid import uuid4

from passlib.hash import sha512_crypt

from marshmallow import Schema, fields, validate


class User(Schema):
    """Definition for user schema."""

    # TODO: add keywords and notifications?

    _id = fields.Method('get_new_uuid')
    name = fields.Str(required=True)
    password = fields.Method('get_encoded_password')
    email = fields.Email(required=True)
    role = fields.Str(
        required=True,
        default='creator',
        validate=validate.OneOf(['administrator', 'expert', 'creator'])
    )
    status = fields.Str(
        required=True,
        default='pending',
        validate=validate.OneOf(['accepted', 'rejected', 'pending'])
    )
    created = fields.Method('get_now')
    modified = fields.Method('get_now')
    deleted = fields.Boolean(required=True, default=False)
    validated = fields.Boolean(required=True, default=False)
    last_activity = fields.Method('get_now')

    def get_now(self, obj):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_new_uuid(self, obj):
        return str(uuid4())

    def get_encoded_password(self, obj):
        return sha512_crypt.hash(
            obj['password'],
            salt='dqwjfdsakuyfd'
        )
