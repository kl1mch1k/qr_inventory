from flask import render_template, request, abort
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from data import db_session
from data.history import History
from data.objects import Object
from data.places import Place
from forms.object_form import ObjForm
from flask_app import app


@app.route('/')
def all_objects():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        objects = db_sess.query(Object)
        places = db_sess.query(Place)
        return render_template("objects.html", objects=objects, places=places)
    else:
        return redirect('/login')


@app.route('/add_object', methods=['GET', 'POST'])
@login_required
def add_object():
    form = ObjForm()
    form.obj_place.choices = ['Не указано'] + [place.text for place in
                                               db_session.create_session().query(Place).all()]
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        obj = Object(name=form.name.data,
                     serial_number=form.serial_number.data)
        if form.obj_place.data != 'Не указано':
            obj.obj_place = db_sess.query(Place).filter(Place.text == form.obj_place.data).first().id
        db_sess.add(obj)
        db_sess.commit()
        return redirect('/')
    return render_template('add_object.html', title='Добавление объекта', form=form)


@app.route('/object/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_object(id):
    form = ObjForm()
    form.obj_place.choices = [(str(i), str(i)) for i in (['Не указано'] +
                                                         [place.text for place in
                                                          db_session.create_session().query(Place).all()])]
    if request.method == "GET":
        db_sess = db_session.create_session()
        obj = db_sess.query(Object).filter(Object.id == id).first()
        if obj:
            if db_sess.query(Place).get(obj.obj_place):
                form = ObjForm(obj_place=db_sess.query(Place).get(obj.obj_place).text)
                form.obj_place.choices = [(str(i), str(i)) for i in (['Не указано'] +
                                                                     [place.text for place in
                                                                      db_session.create_session().query(Place).all()])]
            form.name.data = obj.name
            form.serial_number.data = obj.serial_number

        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        obj = db_sess.query(Object).filter(Object.id == id).first()
        if obj:
            history = History(old_place_id=obj.obj_place,
                              obj_id=obj.id)
            obj.name = form.name.data
            obj.serial_number = form.serial_number.data
            if form.obj_place.data != 'Не указано':
                obj.obj_place = db_sess.query(Place).filter(Place.text == form.obj_place.data).first().id
                history.new_place_id = obj.obj_place
            db_sess.add(history)
            db_sess.commit()
        else:
            abort(404)
        return redirect('/')
    return render_template('add_object.html',
                           title='Редактирование',
                           form=form
                           )


@app.route('/object_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def object_delete(id):
    db_sess = db_session.create_session()
    obj = db_sess.query(Object).filter(Object.id == id).first()
    if obj:
        db_sess.delete(obj)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/object_history/<int:id>')
@login_required
def object_history(id):
    db_sess = db_session.create_session()
    obj = db_sess.query(Object).filter(Object.id == id).first()
    if obj:
        histories = reversed(db_sess.query(History).filter(History.obj_id == obj.id).all())
        places = db_sess.query(Place)
        return render_template('object_history.html', obj=obj, places=places, histories=histories,
                               title='Просмотр истории')
    else:
        abort(404)
