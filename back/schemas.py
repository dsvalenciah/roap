from marshmallow import fields, Schema, ValidationError, validate

class Publication(Schema):
    _id = fields.UUID(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    expert_rating = fields.Integer(
        default=1,
        validate=validate.Range(min=1, max=5)
    )
    general_rating = fields.Integer(
        default=1,
        validate=validate.Range(min=1, max=5)
    )
    # _type = fields.Select(['zip', 'html'])
    _type = fields.Str(required=True)
    files_path = fields.Str()
    tags = fields.List(fields.Str())
    # state = fields.Select(['unevaluated', 'evaluated'])
    state = fields.Str(required=True)

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
    publications = fields.Nested(Publication())
