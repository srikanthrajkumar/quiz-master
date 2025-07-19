from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from backend.app.models import User
from flask import jsonify

def current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or not any(role.name == 'admin' for role in user.roles):
            return {'message': 'Admin access required'}, 403

        return fn(*args, **kwargs)
    return wrapper
