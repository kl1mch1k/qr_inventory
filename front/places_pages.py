from flask import render_template, redirect, request, abort
from flask_login import current_user, login_required

from data import db_session
from data.objects import Object
from data.places import Place
from flask_app import app
from forms.place_form import PlaceForm


# @app.route('/places')
# def places():
#     if current_user.is_authenticated:
#         db_sess = db_session.create_session()
#         objects = db_sess.query(Object)
#         places = db_sess.query(Place)
#         places_with_objects = [[place, [obj.name for obj in objects.filter(Object.obj_place == place.id).all()]]
#                                for place in places]
#         return render_template("places.html", places=places_with_objects)
#     else:
#         return redirect('/login')
#
#
# @app.route('/add_place', methods=['GET', 'POST'])
# @login_required
# def add_place():
#     form = PlaceForm()
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         place = Place(text=form.text.data)
#         db_sess.add(place)
#         db_sess.commit()
#         return redirect('/places')
#     return render_template('add_place.html', title='Добавление места', form=form)
#
#
# @app.route('/places/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_place(id):
#     form = PlaceForm()
#     if request.method == "GET":
#         db_sess = db_session.create_session()
#         place = db_sess.query(Place).filter(Place.id == id).first()
#         if place:
#             form.text.data = place.text
#         else:
#             abort(404)
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         place = db_sess.query(Place).filter(Place.id == id).first()
#         if place:
#             place.text = form.text.data
#             db_sess.commit()
#         else:
#             abort(404)
#         return redirect('/places')
#     return render_template('add_place.html',
#                            title='Редактирование',
#                            form=form
#                            )
#
#
# @app.route('/places_delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def place_delete(id):
#     db_sess = db_session.create_session()
#     place = db_sess.query(Place).filter(Place.id == id).first()
#     if place:
#         db_sess.delete(place)
#         db_sess.commit()
#     else:
#         abort(404)
#     return redirect('/places')
