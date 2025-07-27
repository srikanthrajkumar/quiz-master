from flask_restful import Resource
from flask_jwt_extended import jwt_required
from auth import admin_required
from backend.app.models import Subject, Quiz
from backend.app import db
from . import api

class AdminDashboardResource(Resource):
    @jwt_required()
    def get(self):
        subjects = Subject.query.all()
        result = []
        for subject in subjects:
            result.append({
                'id': subject.id,
                'name': subject.name,
                'description': subject.description,
                'chapters': [
                    {
                        'id': chapter.id,
                        'name': chapter.name,
                        'description': chapter.description,
                        'num_quizzes': len(chapter.quizzes)
                    } for chapter in subject.chapters
                ]
            })
        return result, 200


class QuizDashboardResource(Resource):
    @jwt_required()
    def get(self):
        quizzes = db.session.query(Quiz).all()

        result = []
        for quiz in quizzes:
            quiz_data = {
                'id': quiz.id,
                'name': quiz.name,
                'date_of_quiz': str(quiz.date_of_quiz),
                'time_duration': quiz.time_duration,
                'questions': [
                    {
                        'id': question.id,
                        'question_statement': question.question_statement,
                        'option1': question.option1,
                        'option2': question.option2,
                        'option3': question.option3,
                        'option4': question.option4,
                        'correct_option_index': question.correct_option_index
                    }
                    for question in quiz.questions
                ]
            }
            result.append(quiz_data)

        return result, 200

class UserDashboardResource(Resource):
    @jwt_required()
    def get(self):
        quizzes = db.session.query(Quiz).all()
        
        result = []
        for quiz in quizzes:
            quiz_data = {
                'id': quiz.id,
                'name': quiz.name,
                'date_of_quiz': quiz.date_of_quiz.strftime('%d/%m/%Y'),
                'time_duration': quiz.time_duration.isoformat(),
                'remarks': quiz.remarks,
                'num_questions': len(quiz.questions)
            }
            result.append(quiz_data)

        return result, 200

api.add_resource(UserDashboardResource, '/api/user/quizzes')
api.add_resource(QuizDashboardResource, '/api/admin/quizview')
api.add_resource(AdminDashboardResource, '/api/admin/dashboard')
