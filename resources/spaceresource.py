from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional

from models.space import Space
from schemas.spaceschema import SpaceSchema

from resources.user import UserResource

space_schema = SpaceSchema()
space_list_schema = SpaceSchema(many=True)


class SpaceListResource(Resource):

    @jwt_required
    def get(self): # toimii
        spaces = Space.get_all_published()

        return space_list_schema.dump(spaces).data, HTTPStatus.OK

    @jwt_required
    def post(self): # toimii
        json_data = request.get_json()
        current_user = get_jwt_identity()

        data, errors = space_schema.load(data=json_data)

        if errors:
            return {'message': "Validation errors", 'errors': errors}, HTTPStatus.BAD_REQUEST

        space = Space(**data)
        space.user_id = current_user
        space.save()

        return space_schema.dump(space).data, HTTPStatus.CREATED


class SpaceResource(Resource):

    @jwt_required # toimii
    def patch(self, space_id):
        json_data = request.get_json()

        data, errors = space_schema.load(data=json_data, partial=('name',))

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        space = Space.get_by_id(space_id=space_id)

        if space is None:
            return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND

        space.name = data.get('name') or space.name

        space.save()

        return space_schema.dump(space).data, HTTPStatus.OK

    @jwt_required # toimii
    def get(self, space_id):
        space = Space.get_by_id(space_id=space_id)

        if space is None:
            return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND

        return space_schema.dump(space).data, HTTPStatus.OK

    @jwt_required # toimii
    def delete(self, space_id):
        space = Space.get_by_id(space_id=space_id)

        if space is None:
            return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND

        space.delete()

        return {}, HTTPStatus.NO_CONTENT