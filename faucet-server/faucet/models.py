from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired
)

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User %r>' % self.username


class Data(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    key = db.Column(db.String(length=255), nullable=False)
    value = db.Column(db.Float(), nullable=False)
    units = db.Column(db.String(length=255), nullable=False)
    sensor = db.Column(db.String(length=255), nullable=False)

    location_id = db.Column(
        "location",
        db.Integer(),
        db.ForeignKey("location.id"),
        nullable=False
    )
    location = db.relationship("Location", backref="data")

    host_id = db.Column(db.String(length=255), nullable=False)
    host_machine_type = db.Column(db.String(length=255), nullable=False)
    host_software_version = db.Column(db.String(length=255), nullable=False)
    timestamp = db.Column(db.TIMESTAMP(), nullable=False)

    def __repr__(self):
        return '<Data, key: {} value: {}, host: {}>'.format(
            self.key, self.value, self.host
        )


class Location(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    site = db.Column(db.String(length=255), nullable=False)
    building = db.Column(db.String(length=255), nullable=False)
    room = db.Column(db.String(length=255), nullable=False)
    coordinates = db.Column(db.String(length=255), nullable=True)

    def __repr__(self):
        return '<Location, building: {} room: {}>'.format(
            self.building, self.room
        )
