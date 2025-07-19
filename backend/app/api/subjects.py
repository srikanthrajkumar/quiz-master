from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required
from backend.app.models import Subject
from backend.app import db
from . import api
from auth import admin_required

subject_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
}

subject_parser = reqparse.RequestParser()
subject_parser.add_argument('name', type=str, required=True, help='Subject name is required')
subject_parser.add_argument('description', type=str, required=False)

class SubjectListResource(Resource):
    @jwt_required()
    @marshal_with(subject_fields)
    def get(self):
        return Subject.query.all()
        
    @jwt_required()
    @admin_required
    @marshal_with(subject_fields)
    def post(self):
        args = subject_parser.parse_args()
        if Subject.query.filter_by(name=args['name']).first():
            return {'message': 'Subject already exists'}, 400

        subject = Subject(name=args['name'], description=args.get('description'))
        db.session.add(subject)
        db.session.commit()
        return subject, 201

class SubjectResource(Resource):
    @marshal_with(subject_fields)
    def get(self, subject_id):
        subject = db.session.get(Subject, subject_id)
        if subject is None:
            return {'message': 'Subject not found'}, 404
        return subject

api.add_resource(SubjectListResource, '/api/subjects')
api.add_resource(SubjectResource, '/api/subjects/<int:subject_id>')
