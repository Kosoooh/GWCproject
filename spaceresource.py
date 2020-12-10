from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.space import Space, space_list


class SpaceListResource(Resource):

    def get(self):
        data = []

        for space in space_list:
            if space.is_publish is True:
                data.append(space.data)

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        space = Space(name=data['name'],
                      reservations=data['reservations'])

        space_list.append(space)

        return space.data, HTTPStatus.CREATED


class SpaceResource(Resource):

    def get(self, space_id):
        space = next((space for space in space_list if space.id == space_id and space.is_publish == True), None)

        if space is None:
            return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND

        return space.data, HTTPStatus.OK

    def put(self, space_id):
        data = request.get_json()

        space = next((space for space in space_list if space.id == space_id), None)

        if space is None:
            return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND

        space.name = data['name']

        return space.data, HTTPStatus.OK

    def delete(self, space_id):
        space = next((space for space in space_list if space.id == space_id), None)

        if space is None:
            return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND

        space_list.remove(space)

        return {}, HTTPStatus.NO_CONTENT


class SpacePublishResource(Resource):

    def put(self, space_id):
        space = next((space for space in space_list if space.id == space_id), None)

        if space is None:
            return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND

        space.is_publish = True

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, space_id):
        space = next((space for space in space_list if space.id == space_id), None)

        if space is None:
            return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND

        space.is_publish = False

        return {}, HTTPStatus.NO_CONTENT