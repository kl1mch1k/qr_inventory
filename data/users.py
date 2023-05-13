import sqlalchemy
from flask import jsonify
from flask_login import current_user, UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase, create_session


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    role = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('roles.id'))

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def is_admin(self):
        if str(self.role) == '1':
            return True


class Role(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'roles'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                             index=True, unique=True)


def role_required(role):
    def role_decorator(func):
        def _wrap(*args, **kwargs):
            if create_session().query(Role).filter(Role.name == role).first().id != current_user.role:
                return jsonify({'error': f"{current_user.email} hasn't got enough rights"})
            else:
                return func(*args, **kwargs)

        _wrap.__name__ = func.__name__
        return _wrap
    return role_decorator
