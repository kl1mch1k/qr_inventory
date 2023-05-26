import base64
import os

import requests
from flask import render_template, request, abort, send_file
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from data import db_session
from data.history import History
from data.objects import Object
from data.places import Place
from data.users import role_required, User
from flask_app import app
from forms.object_form import ObjForm
from forms.place_form import PlaceForm


@app.route('/admin/download_qr')
def download():
    if current_user.is_authenticated:
        file = open('temp/temp.xlsx', 'wb')
        file.write(base64.b64decode(requests.get(f'http://127.0.0.1:27016/api/get_xlsx_qr').json()['xlsx'][2:-1]))
        return send_file('temp/temp.xlsx', as_attachment=True)
    else:
        return redirect('/login')


@app.route('/admin/')
@login_required
@role_required('admin')
def admin_all_objects():
    db_sess = db_session.create_session()
    objects = db_sess.query(Object)
    places = db_sess.query(Place)
    users = db_sess.query(User)
    return render_template("admin/main_page.html", objects=objects, places=places, users=users, admin=True,
                           title='QR-inventory')


@app.route('/admin/<int:id>')
@login_required
@role_required('admin')
def admin_place_objects(id):
    db_sess = db_session.create_session()
    objects = db_sess.query(Object).filter(Object.obj_place == id)
    places = db_sess.query(Place)
    return render_template("admin/main_page.html", objects=objects, places=places, title='QR-inventory')


@app.route('/admin/add_object', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin_add_object():
    form = ObjForm()
    form.obj_place.choices = ['Не указано'] + [place.text for place in
                                               db_session.create_session().query(Place).all()]
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        obj = Object(name=form.name.data,
                     serial_number=form.serial_number.data)
        file = form.image.data
        if file:
            file.save(f'images/{str(int(db_sess.query(Object).all()[-1].id) + 1)}.jpg')
        if form.obj_place.data != 'Не указано':
            obj.obj_place = db_sess.query(Place).filter(Place.text == form.obj_place.data).first().id
            if form.obj_responsible.data:
                obj.appoint_responsible(form.obj_responsible.data)
        db_sess.add(obj)
        db_sess.commit()
        return redirect('/admin')
    return render_template('admin/add_object.html', title='Добавление объекта', form=form, editing=False)


@app.route('/admin/object/<int:id>', methods=['GET', 'POST'])
@role_required('admin')
@login_required
def admin_edit_object(id):
    form = ObjForm()
    form.obj_place.choices = [(str(i), str(i)) for i in (['Не указано'] +
                                                         [place.text for place in
                                                          db_session.create_session().query(Place).all()])]
    form.obj_responsible.choices = [(None, 'Не указано')] + [(user.id, user.name) for user in
                                                             db_session.create_session().query(
                                                                 User).filter(User.role != 1)]

    if request.method == "GET":
        db_sess = db_session.create_session()
        obj = db_sess.query(Object).filter(Object.id == id).first()
        if obj:
            file = form.image.data
            if file:
                file.save(f'images/{obj.id}.jpg')
            if db_sess.query(Place).get(obj.obj_place):
                form = ObjForm(obj_place=db_sess.query(Place).get(obj.obj_place).text)
                form.obj_place.choices = [(str(i), str(i)) for i in (['Не указано'] +
                                                                     [place.text for place in
                                                                      db_session.create_session().query(Place).all()])]
            form.name.data = obj.name
            form.serial_number.data = obj.serial_number
            form.obj_responsible.data = obj.responsible_id

        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        obj = db_sess.query(Object).filter(Object.id == id).first()
        if obj:
            file = form.image.data
            if file:
                file.save(f'images/{obj.id}.jpg')
            obj.name = form.name.data
            obj.serial_number = form.serial_number.data
            if form.obj_responsible.data != 'None':
                obj.responsible_id = form.obj_responsible.data

            if str(form.obj_place.data) != str(obj.obj_place) and str(form.obj_place.data) != 'Не указано':
                new_place_id = db_sess.query(Place).filter(Place.text == form.obj_place.data).first().id
                history = History(old_place_id=obj.obj_place,
                                  obj_id=obj.id,
                                  new_place_id=new_place_id)
                db_sess.add(history)
                obj.obj_place = new_place_id
            db_sess.commit()
        else:
            abort(404)
        return redirect('/admin')
    if str(obj.id) in [i.split('.')[0] for i in os.listdir('images')]:
        img = True
    else:
        img = False
    return render_template('admin/add_object.html', img=img,
                           title='Редактирование',
                           form=form,
                           obj_id=obj.id,
                           editing=True
                           )


@app.route('/admin/object_delete/<int:id>', methods=['GET', 'POST'])
@role_required('admin')
@login_required
def admin_object_delete(id):
    db_sess = db_session.create_session()
    obj = db_sess.query(Object).filter(Object.id == id).first()
    if obj:
        db_sess.delete(obj)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/admin')


@app.route('/admin/object_history/<int:id>')
@role_required('admin')
@login_required
def admin_object_history(id):
    db_sess = db_session.create_session()
    obj = db_sess.query(Object).filter(Object.id == id).first()
    if obj:
        histories = reversed(db_sess.query(History).filter(History.obj_id == obj.id).all())
        places = db_sess.query(Place)
        return render_template('object_history.html', obj=obj, places=places, histories=histories,
                               title='Просмотр истории')
    else:
        abort(404)


#
# @app.route('/admin/places')
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


@app.route('/admin/add_place', methods=['GET', 'POST'])
@login_required
def add_place():
    form = PlaceForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        place = Place(text=form.text.data)
        db_sess.add(place)
        db_sess.commit()
        return redirect('/admin')
    return render_template('admin/add_place.html', title='Добавление места', form=form)

# @app.route('/admin/places/<int:id>', methods=['GET', 'POST'])
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
