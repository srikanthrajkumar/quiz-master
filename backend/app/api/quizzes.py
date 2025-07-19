from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required
from datetime import datetime, time
from backend.app.models import Chapter, Quiz
from backend.app import db
from . import api
from auth import admin_required

quiz_fields = {
    'id': fields.Integer,
    'chapter_id': fields.Integer,
    'date_of_quiz': fields.DateTime,
    'time_duration': fields.String,
    'remarks': fields.String,
}

quiz_parser = reqparse.RequestParser()
quiz_parser.add_argument('date_of_quiz', type=str, required=True, help='Date of quiz is required')
quiz_parser.add_argument('time_duration', type=str, required=True, help='Time duration is required')
quiz_parser.add_argument('remarks', type=str, required=False)

class QuizListResource(Resource):
    @jwt_required()
    @marshal_with(quiz_fields)
    def get(self, chapter_id):
        chapter = db.session.get(Chapter, chapter_id)
        if not chapter:
            return {'message': 'Chapter not found'}, 404
        return chapter.quizzes

    @jwt_required()
    @admin_required
    @marshal_with(quiz_fields)
    def post(self, chapter_id):
        chapter = db.session.get(Chapter, chapter_id)
        if not chapter:
            return {'message': 'Chapter not found'}, 404

        args = quiz_parser.parse_args()

        quiz = Quiz(chapter_id=chapter_id, date_of_quiz=datetime.strptime(args['date_of_quiz'], '%d/%m/%Y'), time_duration=time.fromisoformat(args['time_duration']), remarks=args.get('remarks'))

        db.session.add(quiz)
        db.session.commit()
        return quiz, 201

api.add_resource(QuizListResource, '/api/chapters/<int:chapter_id>/quizzes')
