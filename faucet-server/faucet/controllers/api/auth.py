from pymysql.err import OperationalError
from flask import abort, current_app
from flask_restful import Resource

from .parser import user_post_parser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm.exc import NoResultFound

from faucet.models import User


class AuthApi(Resource):
    def post(self):
        args = user_post_parser.parse_args()

        try:
            user = User.query.filter_by(
                username=args['username']
            ).one()
        except NoResultFound:
            abort(401)
        except OperationalError:
            abort(500)

        if user.check_password(args['password']):
            s = Serializer(
                current_app.config['SECRET_KEY'],
                expires_in=600
            )
            return {"token": s.dumps({'id': user.id})}
        else:
            abort(401)
