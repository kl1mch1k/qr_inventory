from flask import jsonify, request

from . import db_session
from .objects import Object

from .api_blueprint import blueprint


@blueprint.route('/api/objects', methods=['GET'])
def get_objects():
    db_sess = db_session.create_session()
    objects = db_sess.query(Object).all()
    return jsonify({
        'objects':
            [item.to_dict()
             for item in objects]
    })


@blueprint.route('/api/objects/<int:obj_id>', methods=['GET'])
def get_one_objects(obj_id):
    db_sess = db_session.create_session()
    object = db_sess.query(Object).get(obj_id)
    if not object:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'objects': object.to_dict()
        }
    )


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


@blueprint.route('/api/jobs/<int:obj_id>', methods=['DELETE'])
def delete_object(obj_id):
    db_sess = db_session.create_session()
    db_sess.execute('PRAGMA foreign_keys = ON;')
    obj = db_sess.query(Object).get(obj_id)
    if not obj:
        return jsonify({'error': 'Not found'})
    db_sess.delete(obj)
    db_sess.commit()
    return jsonify({'success': 'OK'})
