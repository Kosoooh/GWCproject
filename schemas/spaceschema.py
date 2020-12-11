from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema
#from schemas.reservations import ReservationSchema


class SpaceSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    #reservations = fields.Nested(ReservationSchema, attribute='reservation', dump_only=True, only=[TÄHÄN MITKÄ HALUTAAN NÄHDÄ])
    #reservable = fields.Nested(ReservationSchema, attribute='reservation', dump_only=True, only=['id', 'JOTAIN MIKÄ TULEE RESERVATIONSCHEMASTA'])
    is_publish = fields.Boolean(dump_only=True)

    author = fields.Nested(UserSchema, attribute='user', dump_only=True, exclude=('email', ))

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}

        return data
