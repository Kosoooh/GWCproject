from schemas.user import UserSchema
from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError


class ReservationSchema(Schema):
    class Meta:
        ordered = True
    id = fields.Integer(dump_only=True)
    reservationTime = fields.String(required=True, validate=[validate.Length(max=100)])
    is_published= fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    reserved_by = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'username'])

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {"data": data}
        return data
