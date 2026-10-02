from flask import Flask
from .storage import Storage
from .routes import bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['STORAGE'] = Storage('/workspace/sprat.db')
    app.register_blueprint(bp)
    return app
