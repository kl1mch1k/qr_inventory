from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileField, FileAllowed
from data import db_session
from data.places import Place
from data.users import User


class ObjForm(FlaskForm):
    name = StringField('Наименование', validators=[DataRequired()])
    serial_number = StringField('Инв. №', validators=[DataRequired()])
    submit = SubmitField('Принять')
    obj_place = SelectField('Место', choices=([(None, 'Не указано')] + [(place.id, place.text) for place in
                                                                        db_session.create_session().query(
                                                                            Place).all()]))
    obj_responsible = SelectField('Ответсвенный', choices=([(None, 'Не указано')] +
                                                           [(user.id, user.name) for user in
                                                            db_session.create_session().query(
                                                                User).filter(User.role != 1)]), validators=[Optional()])
    image = FileField('Загрузить изображение', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'])])
