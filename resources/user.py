from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from flask import request
from http import HTTPStatus
from flask_restful import Resource
from utils import hash_password

from schemas.user import UserSchema
from schemas.spaceschema import SpaceSchema
from schemas.reservation import ReservationSchema

from webargs import fields
from webargs.flaskparser import use_kwargs

from models.space import Space
from models.reservation import Reservation
from models.user import User

space_list_schema = SpaceSchema(many=True)
reservation_list_schema = ReservationSchema(many=True)
user_schema = UserSchema()
reservation_schema = ReservationSchema()


class UserReservationListResource(Resource):
    @jwt_required
    @use_kwargs({"visibility": fields.Str(missing="public")})
    def get(self, username, visibility):

        user = User.get_by_username(username=username)

        if user is None:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id and visibility in ["all", "private"]:
            pass

        reservations = Reservation.get_all_by_user(user_id=user.id, visibility=visibility)

        return reservation_list_schema.dump(reservations, many=True).data, HTTPStatus.OK


class UserResource(Resource):
    @jwt_required
    def get(self, username): # toimii
        user = User.get_by_username(username=username)

        if user is None:
            return {"message": "user not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:  # User can only get his own account information.
            data = reservation_schema.dump(user).data

        else:
            data = {"message": "method not allowed"}, HTTPStatus.FORBIDDEN

        return data, HTTPStatus.OK

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        data, errors = user_schema.load(data=json_data)

        # Validating the data in users request
        if errors:
            return {"message": "Validation errors", "errors": errors}, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get("username")):
            return {"message": "Username already exists"}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get("email")):
            return {"message": "Email already used"}, HTTPStatus.BAD_REQUEST

        # Creating a user instance
        user = User(**data)
        # Save to db
        user.save()

        # Return successfully registered data
        return user_schema.dump(user).data, HTTPStatus.CREATED


class MeResource(Resource): # Users can check their reservations with this

    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())

        instructions = Reservation.get_all_by_user(user_id=user.id)

        return reservation_list_schema.dump(instructions).data, HTTPStatus.OK
