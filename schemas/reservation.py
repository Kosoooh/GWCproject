from schemas.user import UserSchema
from schemas.spaceschema import SpaceSchema
from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError


def validate_reservationTime(n):  # funktio datan validoinnille
    if n < "16":
        raise ValidationError("Reservable times are from 16 to 21")
    if n > "21":
        raise ValidationError("Reservable times are from 16 to 21")


class ReservationSchema(Schema):
    class Meta:
        ordered = True
    id = fields.Integer(dump_only=True)
    reservationTime = fields.String(required=True, validate=validate_reservationTime)
    is_published= fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    roomID = fields.Nested(SpaceSchema, attribute="space", dump_only=True, only=["id"])
    reserved_by = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'username'])

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {"data": data}
        return data
