# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
socketio = SocketIO()  # Initialize SocketIO

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    socketio.init_app(app)  # Initialize SocketIO with the app

    from app import routes, models
    app.register_blueprint(routes.bp)

    return app
