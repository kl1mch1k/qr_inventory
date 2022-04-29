from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField, SelectField
from wtforms.validators import DataRequired

from data import db_session
from data.places import Place


class ObjForm(FlaskForm):
    name = StringField('Наименование', validators=[DataRequired()])
    serial_number = StringField('Инв. №', validators=[DataRequired()])
    submit = SubmitField('Принять')
    obj_place = SelectField('Место', choices=[(str(i), str(i)) for i in (['Не указано'] +
                                                                         [place.text for place in
                                                                          db_session.create_session().query(
                                                                              Place).all()])])
