#! ../env/bin/python
# -*- coding: utf-8 -*-

import pytest
import datetime

from faucet.models import db, User, Location, Data

create_user = False


@pytest.mark.usefixtures("testapp")
class TestModels:
    def test_user_save(self, testapp):
        """ Test Saving the user model to the database """

        admin = User('admin', 'supersafepassword')
        db.session.add(admin)
        db.session.commit()

        user = User.query.filter_by(username="admin").first()
        assert user is not None

    def test_user_password(self, testapp):
        """ Test password hashing and checking """

        admin = User('admin', 'supersafepassword')

        assert admin.username == 'admin'
        assert admin.check_password('supersafepassword')

    def test_location_save(self, testapp):
        """ Test Saving the location model to the database """

        loc = Location()
        loc.site = "Home"
        loc.building = "main"
        loc.room = "family room"
        db.session.add(loc)
        db.session.commit()

        l = Location.query.filter_by(site="Home").first()
        assert l is not None

    def test_data_save(self, testapp):
        """ Test Saving the data model to the database """

        loc = Location()
        loc.site = "Home"
        loc.building = "main"
        loc.room = "family room"

        d = Data()
        d.key = "temperature"
        d.value = 77
        d.units = "F"
        d.sensor = "test"
        d.location = loc
        d.host_id = "test"
        d.host_machine_type = "tester"
        d.host_software_version = "0000"
        d.timestamp = datetime.datetime.now()

        db.session.add(loc)
        db.session.add(d)
        db.session.commit()

        data = Data.query.filter_by(key="temperature").first()
        assert data is not None
