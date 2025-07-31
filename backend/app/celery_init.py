from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from . import db, migrate

def create_celery_app():
    app = Flask(__name__, instance_relative_config=True)

    db_path = os.path.join(app.instance_path, 'quizmaster.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'super-secret'
    
    os.makedirs(app.instance_path, exist_ok=True)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    return app

_celery_app = None

def get_celery_app():
    global _celery_app
    if _celery_app is None:
        _celery_app = create_celery_app()
    return _celery_app