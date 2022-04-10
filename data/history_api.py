import datetime

from flask import jsonify, request

from . import db_session
from .history import History

from .api_blueprint import blueprint


@blueprint.route('/api/history', methods=['GET'])
def get_history():
    db_sess = db_session.create_session()
    history = db_sess.query(History).all()
    return jsonify({
        'history':
            [item.to_dict()
             for item in history]
    })


@blueprint.route('/api/history/<int:id>', methods=['GET'])
def get_one_history(id):
    db_sess = db_session.create_session()
    history = db_sess.query(History).get(id)
    if not history:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'history': history.to_dict()
        }
    )


# Important! date must be in timestamp format
@blueprint.route('/api/history', methods=['POST'])
def create_history():
    if not request.data:
        return jsonify({'error': 'Empty request'})
    if not all(key in request.json for key in
               ['place_id', 'obj_id']):
        return jsonify({'error': 'Bad request'})
    date = request.json.get('date')
    if date:
        date = datetime.datetime.fromtimestamp(date)
    db_sess = db_session.create_session()
    history = History(place_id=request.json['place_id'],
                      date=date,
                      obj_id=request.json['obj_id'])

    db_sess.add(history)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/history/<int:id>', methods=['DELETE'])
def delete_history(id):
    db_sess = db_session.create_session()
    history = db_sess.query(History).get(id)
    if not history:
        return jsonify({'error': 'Not found'})
    db_sess.delete(history)
    db_sess.commit()
    return jsonify({'success': 'OK'})
