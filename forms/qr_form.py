
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField, widgets

from data import db_session
from data.places import Place


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class QrForm(FlaskForm):
    places = MultiCheckboxField('Локация', choices=([(0, 'Все')] + [(place.id, place.text) for place in
                                                                        db_session.create_session().query(
                                                                            Place).all()]), coerce=int)
    submit = SubmitField('Загрузить')

