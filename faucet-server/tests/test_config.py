#! ../env/bin/python
# -*- coding: utf-8 -*-
from faucet import create_app
from faucet.extensions import rest_api


class TestConfig:
    def test_dev_config(self):
        """ Tests if the development config loads correctly """

        rest_api.resources = []
        app = create_app('faucet.settings.DevConfig')

        assert app.config['DEBUG'] is True
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///../database.db'
        assert app.config['CACHE_TYPE'] == 'null'

    def test_test_config(self):
        """ Tests if the test config loads correctly """

        rest_api.resources = []
        app = create_app('faucet.settings.TestConfig')

        assert app.config['DEBUG'] is True
        assert app.config['SQLALCHEMY_ECHO'] is True
        assert app.config['CACHE_TYPE'] == 'null'

    def test_prod_config(self):
        """ Tests if the production config loads correctly """

        rest_api.resources = []
        app = create_app('faucet.settings.ProdConfig')

        assert app.config['DEBUG'] is False
        assert app.config['CACHE_TYPE'] == 'simple'
