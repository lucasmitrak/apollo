from pymysql.err import OperationalError
from flask import abort
from flask_restful import Resource, fields, marshal_with

from .parser import location_get_parser, location_post_parser
from faucet.models import db, Location, User


location_fields = {
    'site': fields.String(),
    'building': fields.String(),
    'room': fields.String(),
    'coordinates': fields.String()
}


class LocationApi(Resource):
    @marshal_with(location_fields)
    def get(self):
        args = location_get_parser.parse_args(strict=True)

        user = None
        try:
            user = User.verify_auth_token(args['token'])
        except OperationalError:
            abort(500)

        if not user:
            abort(401)

        locations = None
        try:
            locations = Location.query.all()
        except OperationalError:
            abort(500)

        return locations

    def post(self):
        args = location_post_parser.parse_args(strict=True)

        user = None
        try:
            user = User.verify_auth_token(args['token'])
        except OperationalError:
            abort(500)

        if not user:
            abort(401)

        new_loc = Location()

        new_loc.site = args['site']
        new_loc.building = args['building']
        new_loc.room = args['room']

        db.session.add(new_loc)
        db.session.commit()
        return new_loc.id, 201
