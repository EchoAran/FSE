from flask import Flask
from .storage import Storage
from .routes import bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gamma-j-demo'
    app.config['STORAGE_PATH'] = 'data/store.json'
    storage = Storage(app.config['STORAGE_PATH'])
    app.storage = storage
    app.register_blueprint(bp)
    return app
