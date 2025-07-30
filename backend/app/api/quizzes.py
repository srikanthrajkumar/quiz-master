from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required
from datetime import datetime, time
from backend.app.models import Chapter, Quiz
from backend.app import db, cache
from . import api
from auth import admin_required

quiz_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'chapter_id': fields.Integer,
    'date_of_quiz': fields.DateTime,
    'time_duration': fields.String,
    'remarks': fields.String,
}

quiz_parser = reqparse.RequestParser()
quiz_parser.add_argument('name', type=str, required=True, help='Quiz name is required')
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

        quiz = Quiz(name = args['name'], chapter_id=chapter_id, date_of_quiz=datetime.strptime(args['date_of_quiz'], '%d/%m/%Y'), time_duration=time.fromisoformat(args['time_duration']), remarks=args.get('remarks'))

        db.session.add(quiz)
        db.session.commit()

        cache.delete("quiz_dashboard_data")
        cache.delete("user_summary_data")
        cache.delete("admin_summary_data")

        return quiz, 201

class QuizListAllResource(Resource):
    @marshal_with(quiz_fields)
    @jwt_required()
    def get(self):
        return Quiz.query.all(), 200

class QuizResource(Resource):
    @jwt_required()
    @admin_required
    def delete(self, quiz_id):
        quiz = db.session.get(Quiz, quiz_id)
        if not quiz:
            return {'message': 'Quiz not found'}, 404

        db.session.delete(quiz)
        db.session.commit()

        return {'message': 'Quiz deleted successfully'}, 200


api.add_resource(QuizListResource, '/api/chapters/<int:chapter_id>/quizzes')
api.add_resource(QuizListAllResource, '/api/quizzes')
api.add_resource(QuizResource, '/api/quizzes/<int:quiz_id>')