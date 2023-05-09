from flask import Flask, jsonify, make_response
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from data import db_session
from data.db_session import global_init

from data.users import User

global_init('db/inventory_new.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['JWT_SECRET_KEY'] = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
jwt_manager = JWTManager(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# pages are routing here

from front import objects_pages
from front import authorization_pages
from front import places_pages
from front import qr_pages
