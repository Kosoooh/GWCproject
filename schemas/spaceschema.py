from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema


class SpaceSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    reservableTimes = fields.String(validate=[validate.Length(max=100)])
    is_publish = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}

        return data
