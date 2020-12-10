from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from flask import request
from http import HTTPStatus
from flask_restful import Resource
from utils import hash_password

from schemas.user import UserSchema
from schemas.space import SpaceSchema
from schemas.reservation import ReservationSchema

from webargs import fields
from webargs.flaskparser import use_kwargs

from models.space import Space
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
    def get(self, username):
        user = User.get_by_username(username=username)

        if user is None:
            return {"message": "user not found"}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:  # User can only get his own account information.
            data = user_schema.dump(user).data

        # Shouldn't need a "current_user is None" check because we have jwt_required

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


class MeResource(Resource):  # Not necessarily a class that we need but it can be deleted later if we want to

    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())

        return reservation_schema.dump(user).data, HTTPStatus.OK