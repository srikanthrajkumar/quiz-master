from flask_restful import Resource, fields, marshal_with, reqparse
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from datetime import datetime
from backend.app.models import Score, User, Quiz
from backend.app import db
from . import api
from auth import admin_required


score_fields = {
    'id': fields.Integer,
    'quiz_id': fields.Integer,
    'user_id': fields.Integer,
    'time_stamp_of_attempt': fields.DateTime(dt_format='iso8601'),
    'total_scored': fields.Integer,
    'remarks': fields.String,
}

score_parser = reqparse.RequestParser()
score_parser.add_argument('quiz_id', type=int, required=True, help='Quiz ID is required')
score_parser.add_argument('total_scored', type=int, required=True, help='Total score is required')
score_parser.add_argument('remarks', type=str, required=False)

class UserScoreListResource(Resource):
    @jwt_required()
    @marshal_with(score_fields)
    def get(self, user_id):
        scores = Score.query.filter_by(user_id=user_id).all()
        return scores, 200

    @jwt_required()
    @cross_origin()
    @marshal_with(score_fields)
    def post(self, user_id):
        args = score_parser.parse_args()

        user = db.session.get(User, user_id)
        if not user:
            return {'message': 'User not found'}, 404

        quiz = db.session.get(Quiz, args['quiz_id'])
        if not quiz:
            return {'message': 'Quiz not found'}, 404

        existing_score = Score.query.filter_by(user_id=user_id, quiz_id=args['quiz_id']).first()
        if existing_score:
            return {'message': 'Score already exists'}, 409


        score = Score(
            quiz_id=args['quiz_id'],
            user_id=user_id,
            total_scored=args['total_scored'],
            remarks=args.get('remarks'),
            time_stamp_of_attempt=datetime.utcnow()
        )
        db.session.add(score)
        db.session.commit()
        return score, 201
        
    @jwt_required()
    @marshal_with(score_fields)
    def put(self, user_id):
        args = score_parser.parse_args()

        score = Score.query.filter_by(user_id=user_id, quiz_id=args['quiz_id']).first()
        if not score:
            return {'message': 'Score not found for this user and quiz'}, 404

        score.total_scored = args['total_scored']
        score.remarks = args.get('remarks')
        score.time_stamp_of_attempt = datetime.utcnow()
        db.session.commit()
        return score, 200

class UserScoreResource(Resource):
    @jwt_required()
    @admin_required
    def delete(self, score_id):
        score = db.session.get(Score, score_id)
        if not score:
            return {'message': 'Score not found'}, 404

        db.session.delete(score)
        db.session.commit()

        return {'message': 'Score deleted successfully'}, 200

api.add_resource(UserScoreListResource, '/api/users/<int:user_id>/scores')
api.add_resource(UserScoreResource, '/api/scores/<int:score_id>')
