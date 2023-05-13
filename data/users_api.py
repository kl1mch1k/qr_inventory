from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from data import db_session
from data.objects import Object
from data.places import Place
from data.users import User
from flask_app import app



@app.route("/api/users/get_places", methods=["GET"])
@jwt_required()
def user_get_places():
    db_sess = db_session.create_session()
    current_user = db_sess.query(User).filter(User.email==get_jwt_identity()).first()
    places = db_sess.query(Place)
    if current_user.is_admin():
        return jsonify({'places': [place.text for place in places]})
    user_places = set()
    for obj in db_sess.query(Object).filter(Object.responsible_id==current_user.id):
        if places.get(obj.obj_place):
            user_places.add(places.get(obj.obj_place).text)
    return jsonify({'places':list(user_places)})
# @app.route("/protected", methods=["GET"])
# @jwt_required()
# def protected():
#     # Access the identity of the current user with get_jwt_identity
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200
