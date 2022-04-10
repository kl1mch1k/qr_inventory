import datetime

import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class History(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'history'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    place_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('places.id'))
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    obj_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('objects.id'))

