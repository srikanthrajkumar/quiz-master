from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required
from backend.app.models import Question, Quiz
from backend.app import db
from . import api
from auth import admin_required

question_fields = {
    'id': fields.Integer,
    'quiz_id': fields.Integer,
    'question_statement': fields.String,
    'option1': fields.String,
    'option2': fields.String,
    'option3': fields.String,
    'option4': fields.String,
    'correct_option_index': fields.Integer,
    'photoURL': fields.String,
}

question_parser = reqparse.RequestParser()
question_parser.add_argument('question_statement', type=str, required=True, help='Question is required')
question_parser.add_argument('option1', type=str, required=True, help='Option 1 is required')
question_parser.add_argument('option2', type=str, required=True, help='Option 2 is required')
question_parser.add_argument('option3', type=str)
question_parser.add_argument('option4', type=str)
question_parser.add_argument('correct_option_index', type=int, required=True, help='Correct option index is required')
question_parser.add_argument('photoURL', type=str)

class QuestionListResource(Resource):
    @jwt_required()
    @marshal_with(question_fields)
    def get(self, quiz_id):
        return Question.query.filter_by(quiz_id=quiz_id).all()

    @jwt_required()
    @admin_required
    @marshal_with(question_fields)
    def post(self, quiz_id):
        if not db.session.get(Quiz, quiz_id):
            return {'message': 'Quiz not found'}, 404

        args = question_parser.parse_args()
        question = Question(quiz_id=quiz_id,
            question_statement=args['question_statement'],
            option1=args['option1'],
            option2=args['option2'],
            option3=args.get('option3'),
            option4=args.get('option4'),
            correct_option_index=args['correct_option_index'],
            photoURL=args.get('photoURL')
        )
        db.session.add(question)
        db.session.commit()
        return question, 201

class QuestionResource(Resource):
    @jwt_required()
    @marshal_with(question_fields)
    def get(self, question_id):
        question = db.session.get(Question, question_id)
        if not question:
            return {'message': 'Question not found for this quiz'}, 404
        return question

    @jwt_required()
    @marshal_with(question_fields)
    def put(self, question_id):
        question = db.session.get(Question, question_id)
        if not question:
            return {'message': 'Question not found for this quiz'}, 404

        args = question_parser.parse_args()
        question.question_statement = args['question_statement']
        question.option1 = args['option1']
        question.option2 = args['option2']
        question.option3 = args.get('option3')
        question.option4 = args.get('option4')
        question.correct_option_index = args['correct_option_index']
        question.photoURL = args.get('photoURL')

        db.session.commit()
        return question, 200

    def delete(self, question_id):
        question = db.session.get(Question, question_id)
        if not question:
            return {'message': 'Question not found for this quiz'}, 404

        db.session.delete(question)
        db.session.commit()
        return {'message': 'Question deleted successfully'}, 200

api.add_resource(QuestionListResource, '/api/quizzes/<int:quiz_id>/questions')
api.add_resource(QuestionResource, '/api/questions/<int:question_id>')
