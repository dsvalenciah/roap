from marshmallow import fields, Schema, validate

class LearningObject(Schema):
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