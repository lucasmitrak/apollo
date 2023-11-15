from flask.ext.restful import reqparse

data_post_parser = reqparse.RequestParser()
data_post_parser.add_argument(
    'key',
    type=str,
    required=True,
    help="key is required"
)
data_post_parser.add_argument(
    'value',
    type=float,
    required=True,
    help="value is required"
)
data_post_parser.add_argument(
    'units',
    type=str,
    required=True,
    help="units is required"
)
data_post_parser.add_argument(
    'sensor',
    type=str,
    required=True,
    help="sensor is required"
)
data_post_parser.add_argument(
    'location_id',
    type=str,
    required=True,
    help="location_id is required"
)
data_post_parser.add_argument(
    'host_id',
    type=str,
    required=True,
    help="host_id is required"
)
data_post_parser.add_argument(
    'host_machine_type',
    type=str,
    required=True,
    help="host_machine_type is required"
)
data_post_parser.add_argument(
    'host_software_version',
    type=str,
    required=True,
    help="host_software_version is required"
)
data_post_parser.add_argument(
    'timestamp',
    type=str,
    required=True,
    help="timestamp is required to add data"
)
data_post_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to add data"
)

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('username', type=str, required=True)
user_post_parser.add_argument('password', type=str, required=True)

location_get_parser = reqparse.RequestParser()
location_get_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to get data"
)

location_post_parser = reqparse.RequestParser()
location_post_parser.add_argument('site', type=str, required=True)
location_post_parser.add_argument('building', type=str, required=True)
location_post_parser.add_argument('room', type=str, required=True)
location_post_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to add data"
)
