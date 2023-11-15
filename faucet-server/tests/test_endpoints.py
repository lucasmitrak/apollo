#! ../env/bin/python
# -*- coding: utf-8 -*-

import pytest
import json
import datetime

create_user = True


@pytest.mark.usefixtures("testapp")
class TestEnpoints:
    def test_home(self, testapp):
        """ Tests if the home page loads """

        rv = testapp.get('/')
        assert rv.status_code == 200

    def test_auth_token_api(self, testapp):
        """ test if getting an auth token works """

        rv = testapp.post('/api/v1/auth', data=dict(
            username="admin",
            password="supersafepassword"
        ))
        assert rv.status_code == 200

        a = json.loads(rv.data)
        assert a.get('token')

    def test_auth_token_api_rejection(self, testapp):
        """ test if the auth API rejects bad user data """

        rv = testapp.post('/api/v1/auth', data=dict(
            username="a",
            password="supersafepassword"
        ))
        assert rv.status_code == 401

        rv = testapp.post('/api/v1/auth', data=dict(
            username="admin",
            password=""
        ))
        assert rv.status_code == 401

    def test_data_api(self, testapp):
        """ test if saving using the API works for data """

        token_req = testapp.post('/api/v1/auth', data=dict(
            username="admin",
            password="supersafepassword"
        ))
        token = json.loads(token_req.data).get('token')

        rv = testapp.post('/api/v1/data', data=dict(
            key="temp",
            value=77.2,
            units="F",
            sensor="test",
            location_id=1,
            host_id="test",
            host_machine_type="test",
            host_software_version="test",
            timestamp=datetime.datetime.now(),
            token=token
        ))
        assert rv.status_code == 201

    def test_data_api_rejection(self, testapp):
        """ test if the API rejects a bad token """

        rv = testapp.post('/api/v1/data', data=dict(
            key="temp",
            value=77.2,
            units="F",
            sensor="test",
            location_id=1,
            host_id="test",
            host_machine_type="test",
            host_software_version="test",
            timestamp=datetime.datetime.now(),
            token=""
        ))
        assert rv.status_code == 401

    def test_location_get_api(self, testapp):
        """ test if getting using the API works for locations """

        token_req = testapp.post('/api/v1/auth', data=dict(
            username="admin",
            password="supersafepassword"
        ))
        token = json.loads(token_req.data).get('token')

        rv = testapp.get('/api/v1/location', data=dict(
            token=token
        ))
        result = {
            'building': 'test',
            'room': 'test',
            'site': 'test',
            'coordinates': 'test'
        }

        assert rv.status_code == 200
        assert result == json.loads(rv.data)[0]

    def test_data_post_api(self, testapp):
        """ test if saving using the API works for data """

        token_req = testapp.post('/api/v1/auth', data=dict(
            username="admin",
            password="supersafepassword"
        ))
        token = json.loads(token_req.data).get('token')

        rv = testapp.post('/api/v1/location', data=dict(
            site="test2",
            building="test2",
            room="test2",
            token=token
        ))
        assert rv.status_code == 201

    def test_location_api_get_rejection(self, testapp):
        """ test if the API rejects a bad token """

        rv = testapp.get('/api/v1/location', data=dict(
            token=""
        ))
        assert rv.status_code == 401

    def test_location_api_post_rejection(self, testapp):
        """ test if saving using the API works for data """

        rv = testapp.post('/api/v1/location', data=dict(
            site="test2",
            building="test2",
            room="test2",
            token=""
        ))
        assert rv.status_code == 401
