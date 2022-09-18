from flask import Flask


def create_app():
    app = Flask(__name__)

    # blueprint for auth'd routes in our app
    from .app import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for un-auth parts of app
    from .app import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app