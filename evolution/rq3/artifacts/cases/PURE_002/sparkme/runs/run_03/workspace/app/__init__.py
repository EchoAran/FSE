from flask import Flask
from .state import store
from .routes import bp


def create_app():
    app = Flask(__name__)
    app.secret_key = 'gamma-j-dev-secret'
    app.register_blueprint(bp)
    app.config['STORE'] = store
    return app
