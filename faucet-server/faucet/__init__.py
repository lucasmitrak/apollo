#! ../env/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Jack Stouffer'
__email__ = 'jack@jackstouffer.com'
__version__ = '0.2'

from flask import Flask

from faucet.controllers.main import main
from faucet.models import db
from faucet.controllers.api.data import DataApi
from faucet.controllers.api.auth import AuthApi
from faucet.controllers.api.location import LocationApi

from faucet.extensions import (
    cache,
    login_manager,
    rest_api
)


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. faucet.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    app.config.from_object(object_name)

    # initialize the cache
    cache.init_app(app)

    # initialize SQLAlchemy
    db.init_app(app)

    login_manager.init_app(app)

    rest_api.add_resource(AuthApi, 'auth')
    rest_api.add_resource(DataApi, 'data')
    rest_api.add_resource(LocationApi, 'location')
    rest_api.init_app(app)

    # register our blueprints
    app.register_blueprint(main)

    return app
