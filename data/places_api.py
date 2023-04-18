from flask import jsonify, request

from . import db_session
from .history import History
from .objects import Object
from .places import Place

from .api_blueprint import blueprint


@blueprint.route('/api/places', methods=['GET'])
def get_places():
    db_sess = db_session.create_session()
    places = db_sess.query(Place).all()
    return jsonify({
        'places':
            [item.to_dict()
             for item in places]
    })


@blueprint.route('/api/places/<int:id>', methods=['GET'])
def get_one_place(id):
    db_sess = db_session.create_session()
    place = db_sess.query(Place).get(id)
    if not place:
        return jsonify({'error': 'Not found'})

    return jsonify(
        {
            'places': dict([(str(i), str(j)) for i, j in place.to_dict().items()])
        }
    )


@blueprint.route('/api/places', methods=['POST'])
def create_place():
    if not request.data:
        return jsonify({'error': 'Empty request'})
    if not all(key in request.json for key in
               ['text']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    place = Place(text=request.json['text'])

    db_sess.add(place)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/places/<int:id>', methods=['DELETE'])
def delete_place(id):
    db_sess = db_session.create_session()
    place = db_sess.query(Place).get(id)
    if not place:
        return jsonify({'error': 'Not found'})

    # deleting information about that place in other tables
    for obj in db_sess.query(Object).filter(Object.obj_place == id):
        obj.obj_place = None

    for history in db_sess.query(History).filter(History.place_id == id):
        history.delete()

    db_sess.delete(place)
    db_sess.commit()
    return jsonify({'success': 'OK'})
