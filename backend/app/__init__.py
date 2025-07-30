from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_caching import Cache
from werkzeug.security import generate_password_hash
from .celery_app import init_celery
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cache = Cache()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    CORS(app, origins=["http://127.0.0.1:5173"])

    db_path = os.path.join(app.instance_path, 'quizmaster.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'super-secret'
    app.config['JWT_SECRET_KEY'] = 'jwt-super-secret'
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
    app.config['SECURITY_PASSWORD_SALT'] = 'salty'
    app.config['SECURITY_PASSWORD_SINGLE_HASH'] = False
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
    # app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    # app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cache.init_app(app)

    from .models import User, Role, UserRoles

    admin_username = os.environ.get('ADMIN_USERNAME', 'mcnair')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'major_chandrakant')

    with app.app_context():
        db.create_all()
        
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)
        
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            user_role = Role(name='user')
            db.session.add(user_role)
        
        db.session.commit()
        
        admin_user = User.query.filter_by(username=admin_username).first()
        if not admin_user:
            admin_user = User(
                username=admin_username,
                first_name='Major',
                last_name='Chandrakant',
                qualification='N/A',
                password=generate_password_hash(admin_password),
                active=True,
                fs_uniquifier=admin_username
            )
            db.session.add(admin_user)
            db.session.commit()

            admin_user_role = UserRoles(user_id=admin_user.id, role_id=admin_role.id)
            db.session.add(admin_user_role)
            db.session.commit()

            print("Admin user created with admin role.")
        else:
            print("Admin user already exists.")

    from .api import init_api
    init_api(app)

    @app.route('/api/downloads/<filename>')
    def download_file(filename):
        return send_from_directory(os.path.join(app.instance_path, 'exports'), filename)

    init_celery(app)
    from . import jobs

    return app
