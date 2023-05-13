from data import api_blueprint
from flask_app import app


def main():
    app.register_blueprint(api_blueprint.blueprint)
    app.run(host='0.0.0.0', port=27016)
    # app.run()

if __name__ == '__main__':
    main()
