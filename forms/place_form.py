from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PlaceForm(FlaskForm):
    text = StringField('Наименование места', validators=[DataRequired()])
    submit = SubmitField('Принять')
