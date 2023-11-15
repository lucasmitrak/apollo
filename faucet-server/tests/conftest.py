import pytest

from faucet import create_app
from faucet.models import db, User, Location
from faucet.extensions import rest_api


@pytest.fixture()
def testapp(request):
    rest_api.resources = []
    app = create_app('faucet.settings.TestConfig')
    client = app.test_client()

    db.app = app
    db.create_all()

    if getattr(request.module, "create_user", True):
        admin = User('admin', 'supersafepassword')
        l = Location()
        l.site = "test"
        l.building = "test"
        l.room = "test"
        l.coordinates = "test"

        db.session.add(admin)
        db.session.add(l)
        db.session.commit()

    def teardown():
        db.session.remove()
        db.drop_all()

    request.addfinalizer(teardown)

    return client
