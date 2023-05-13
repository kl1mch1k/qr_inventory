from flask import jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_login import login_required

from . import db_session
from .api_blueprint import blueprint
from .history import History
from .objects import Object
from .places import Place
from .users import User


@blueprint.route('/api/objects', methods=['GET'])
@jwt_required()
def get_objects():
    db_sess = db_session.create_session()
    current_user = db_sess.query(User).filter(User.email==get_jwt_identity()).first()
    if current_user.is_admin():
        objects = db_sess.query(Object).all()
    else:
        objects = db_sess.query(Object).filter(Object.responsible_id==current_user.id).all()
    for i in range(len(objects)):
        obj = objects[i].to_dict()
        if obj.get('obj_place'):
            obj['obj_place_text'] = db_sess.query(Place).get(obj['obj_place']).text
        else:
            obj['obj_place_text'] = None
        objects[i] = dict([(i, str(j)) for i, j in obj.items()])

    return jsonify({
        'objects':
            objects
    })


@blueprint.route('/api/objects/<int:obj_id>', methods=['GET'])
def get_one_object(obj_id):
    db_sess = db_session.create_session()
    object = db_sess.query(Object).get(obj_id)
    if not object:
        return jsonify({'error': 'Not found'})
    object = object.to_dict()
    if object['obj_place']:
        object['obj_place_text'] = db_sess.query(Place).get(object['obj_place']).text
    else:
        object['obj_place_text'] = None

    return jsonify(
        {
            'objects': dict([(i, str(j)) for i, j in object.items()])
        }
    )

@blueprint.route('/api/objects/image/<int:obj_id>', methods=['GET'])
def get_image_object(obj_id):
    return send_file('images/1.JPG')

@blueprint.route('/api/objects', methods=['POST'])
def create_objects():
    if not request.data:
        return jsonify({'error': 'Empty request'})
    if not all(key in request.json for key in
               ['name', 'serial_number']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    obj = Object(name=request.json['name'],
                 serial_number=request.json['serial_number'],
                 obj_place=request.json.get('obj_place'))

    db_sess.add(obj)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/objects/<int:obj_id>', methods=['DELETE'])
def delete_object(obj_id):
    db_sess = db_session.create_session()
    db_sess.execute('PRAGMA foreign_keys = ON;')
    obj = db_sess.query(Object).get(obj_id)
    if not obj:
        return jsonify({'error': 'Not found'})
    db_sess.delete(obj)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/objects/<int:obj_id>', methods=['PATCH'])
def patch_object(obj_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    db_sess = db_session.create_session()
    obj = db_sess.query(Object).get(obj_id)
    if obj:
        if request.json.get('name'):
            obj.name = request.json['name']
        if request.json.get('serial_number'):
            obj.serial_number = request.json['serial_number']
        if request.json.get('obj_place'):
            history = History(old_place_id=obj.obj_place,
                              obj_id=obj.id)
            obj.obj_place = request.json['obj_place']
            history.new_place_id = request.json['obj_place']
            db_sess.add(history)
        if request.json.get('checked'):
            obj.checked = request.json['checked']
        db_sess.commit()
        return jsonify({'success': 'OK'})
    else:
        return jsonify({'error': 'Unknown object ID'})
