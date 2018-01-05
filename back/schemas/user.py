from marshmallow import fields, Schema, validate
from schemas.learning_object import LearningObject

class User(Schema):
    _id = fields.Str(required=True)
    name = fields.Str(required=True)
    email = fields.Str(
        required=True,
        validate=validate.Email(error='Not a valid email address')
    )
    # role = fields.Select(['administrator', 'expert', 'creator', 'external'])
    role = fields.Str(required=True)
    created = fields.Str(required=True, format='%Y-%m-%d %H:%M:%S')
    modified = fields.Str(required=False)
    publications = fields.Nested(LearningObject())
