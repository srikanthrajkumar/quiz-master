from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from backend.app.models import User
from datetime import datetime, timedelta
from backend.app import db
from . import api
from auth import current_user, admin_required

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'qualification': fields.String,
    'active': fields.Boolean
}

register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=str, required=True, help='Username is required')
register_parser.add_argument('first_name', type=str, required=True, help='First Name is required')
register_parser.add_argument('last_name', type=str, required=True, help='Last Name is required')
register_parser.add_argument('qualification', type=str, required=True, help='Qualification is required')
register_parser.add_argument('password', type=str, required=True, help='Password is required')

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)

class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = db.session.get(User, user_id)
        if user is None:
            return {'message': 'User not found'}, 404
        return user

class UserRegisterResource(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = register_parser.parse_args()

        if User.query.filter(User.username == args['username']).first():
            return {'message': 'User with that username exists'}, 400

        user = User(
            username=args['username'],
            first_name=args['first_name'],
            last_name=args['last_name'],
            qualification=args['qualification'],
            password=generate_password_hash(args['password']),
            active=True,
            fs_uniquifier=args['username']
        )

        db.session.add(user)
        db.session.commit()
        return user, 201

class Login(Resource):
    def post(self):
        args = login_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        
        if not user:
            return {'message': f'User {args["username"]} does not exist'}, 404

        if not check_password_hash(user.password, args['password']):
            return {'message': 'Invalid password'}, 403

        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {'access_token': access_token}, 200

    @jwt_required()
    def get(self):
        user = current_user(get_jwt_identity())
        return {'login': True, 'message': f'Logged in as {user.username}'}, 200

api.add_resource(UserResource, '/api/users/<int:user_id>')
api.add_resource(UserRegisterResource, '/api/users/register')
api.add_resource(Login, '/api/users/login')