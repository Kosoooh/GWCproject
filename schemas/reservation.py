from marshmallow import Schema, fields, validate
# from schemas.user import UserSchema
# from schemas.spaceschema import SpaceSchema


class ReservationSchema(Schema):
    class Meta:
        ordered = True
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])

    is_publish = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

#    author = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'username'])
