from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from models.reservation import Reservation
from schemas.reservation import ReservationSchema
from resources.spaceresource import SpaceListResource

reservation_schema = ReservationSchema()
reservation_list_schema = ReservationSchema(many=True)


class ReservationListResource(Resource):

    def get(self): # tällä admin voisi nähdä listan kaikista reservationeista
        reservations = Reservation.get_all_published()

        return reservation_list_schema.dump(reservations).data, HTTPStatus.OK

    @jwt_required
    def post(self): # toimii
        json_data = request.get_json()
        current_user = get_jwt_identity()

        data, errors = reservation_schema.load(data=json_data)

        if errors:
            return {'message': "Validation errors", 'errors': errors}, HTTPStatus.BAD_REQUEST

        reservation = Reservation(**data)
        reservation.user_id = current_user
        reservation.save()

        return reservation_schema.dump(reservation).data, HTTPStatus.CREATED


class ReservationResource(Resource):

    @jwt_required
    def patch(self, reservation_id): # toimii
        json_data = request.get_json()

        data, errors = reservation_schema.load(data=json_data, partial=('name',))

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.reservationTime = data.get('reservationTime') or reservation.reservationTime

        reservation.save()

        return reservation_schema.dump(reservation).data, HTTPStatus.OK

    @jwt_required
    def get(self, reservation_id):  # toimii, muttei välttämättä tarpeellinen
        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if reservation.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return reservation_schema.dump(reservation).data, HTTPStatus.OK

    @jwt_required
    def delete(self, reservation_id):  # toimii
        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.delete()

        return {}, HTTPStatus.NO_CONTENT

