from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from data import db_session
from data.users import User
from flask_app import app


@app.route("/api/login", methods=["POST"])
def api_login():
    if not request.data:
        return jsonify({'error': 'Empty request'})

    if not all(key in request.json for key in
               ['login', 'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == request.json['login']).first()
    if user:
        if user.check_password(request.json['password']):
            access_token = create_access_token(identity=request.json['login'])
            return jsonify(access_token=access_token)
        else:
            return jsonify({'error': 'Wrong password'})
    else:
        return jsonify({'error': 'User not found'})


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
