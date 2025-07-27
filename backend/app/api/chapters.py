from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required
from backend.app.models import Subject, Chapter
from backend.app import db
from . import api
from auth import admin_required

chapter_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'subject_id': fields.Integer,
}

chapter_parser = reqparse.RequestParser()
chapter_parser.add_argument('name', type=str, required=True, help='Name is required')
chapter_parser.add_argument('description', type=str, required=False)

class ChapterListResource(Resource):
    @jwt_required()
    @marshal_with(chapter_fields)
    def get(self, subject_id):
        subject = db.session.get(Subject, subject_id)
        if not subject:
            return {'message': 'Subject not found'}, 404
        return subject.chapters

    @jwt_required()
    @admin_required
    @marshal_with(chapter_fields)
    def post(self, subject_id):
        subject = db.session.get(Subject, subject_id)
        if not subject:
            return {'message': 'Subject not found'}, 404

        args = chapter_parser.parse_args()
        chapter = Chapter(name=args['name'], description=args['description'], subject_id=subject_id)
        db.session.add(chapter)
        db.session.commit()
        return chapter, 201

class ChapterResource(Resource):
    @jwt_required()
    @marshal_with(chapter_fields)
    def get(self, chapter_id):
        chapter = db.session.get(Chapter, chapter_id)
        if not chapter:
            return {'message': 'Chapter not found'}, 404
        return chapter

    @jwt_required()
    @admin_required
    @marshal_with(chapter_fields)
    def put(self, chapter_id):
        chapter = db.session.get(Chapter, chapter_id)
        if not chapter:
            return {'message': 'Chapter not found'}, 404

        args = chapter_parser.parse_args()
        chapter.name = args['name']
        chapter.description = args.get('description')
        db.session.commit()

        return chapter, 200

    @jwt_required()
    @admin_required
    def delete(self, chapter_id):
        chapter = db.session.get(Chapter, chapter_id)
        if not chapter:
            return {'message': 'Chapter not found'}, 404

        db.session.delete(chapter)
        db.session.commit()

        return {'message': 'Chapter deleted successfully'}, 200

class ChapterListAllResource(Resource):
    @marshal_with(chapter_fields)
    @jwt_required()
    def get(self):
        return Chapter.query.all(), 200

api.add_resource(ChapterListResource, '/api/subjects/<int:subject_id>/chapters')
api.add_resource(ChapterListAllResource, '/api/chapters')
api.add_resource(ChapterResource, '/api/chapters/<int:chapter_id>')