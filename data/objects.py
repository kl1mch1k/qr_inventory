import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Object(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'objects'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    serial_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    obj_place = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('places.id'),
                                  nullable=True)
