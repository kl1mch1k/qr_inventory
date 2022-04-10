from flask import Flask, jsonify, make_response

from data.db_session import global_init
from data import api_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# login_manager = LoginManager()
# login_manager.init_app(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    global_init('db/inventory_new.db')
    app.register_blueprint(api_blueprint.blueprint)
    app.run()


if __name__ == '__main__':
    main()
