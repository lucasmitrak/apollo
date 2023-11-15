from pymysql.err import OperationalError
from flask import abort
from flask_restful import Resource
from dateutil.parser import parse

from .parser import data_post_parser
from faucet.models import db, Data, User


class DataApi(Resource):
    def post(self):
        args = data_post_parser.parse_args(strict=True)

        user = None
        try:
            user = User.verify_auth_token(args['token'])
        except OperationalError:
            abort(500)

        if not user:
            abort(401)

        new_data = Data()

        new_data.key = args['key']
        new_data.value = args['value']
        new_data.units = args['units']
        new_data.sensor = args['sensor']
        new_data.location_id = args['location_id']
        new_data.host_id = args['host_id']
        new_data.host_machine_type = args['host_machine_type']
        new_data.host_software_version = args['host_software_version']
        new_data.timestamp = parse(args['timestamp'])

        db.session.add(new_data)
        db.session.commit()
        return new_data.id, 201
