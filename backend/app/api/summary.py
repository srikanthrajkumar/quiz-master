from flask_restful import Resource
from flask_jwt_extended import jwt_required
from backend.app.models import Subject, Chapter, Quiz, Question, Score
from backend.app import db, cache
from . import api
from auth import admin_required

class AdminSummaryResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        cached_data = cache.get("admin_summary_data")
        if cached_data:
            return cached_data, 200

        data = []

        subjects = db.session.query(Subject).all()

        for subject in subjects:
            subject_summary = {
                'subject_name': subject.name,
                'chapter_count': 0,
                'quiz_count': 0,
                'total_attempts': 0,
                'top_score': 0,
                'average_score': 0
            }

            chapters = subject.chapters
            subject_summary['chapter_count'] = len(chapters)

            all_quizzes = []
            for chapter in chapters:
                all_quizzes.extend(chapter.quizzes)
            subject_summary['quiz_count'] = len(all_quizzes)

            quiz_ids = [quiz.id for quiz in all_quizzes]

            if quiz_ids:
                scores = db.session.query(Score).filter(Score.quiz_id.in_(quiz_ids)).all()
                subject_summary['total_attempts'] = len(scores)
                subject_summary['top_score'] = max((s.total_scored or 0) for s in scores) if scores else 0
                subject_summary['average_score'] = round(sum((s.total_scored or 0) for s in scores) / len(scores), 2) if scores else 0

            question_count = db.session.query(Question).join(Quiz).join(Chapter).filter(Chapter.subject_id == subject.id).count()
            subject_summary['question_count'] = question_count

            data.append(subject_summary)

        cache.set("admin_summary_data", data, timeout=60)
        return data, 200

class UserSummaryResource(Resource):
    @jwt_required()
    def get(self, user_id):
        cached_data = cache.get("user_summary_data")
        if cached_data:
            return cached_data, 200
        
        data = []

        subjects = db.session.query(Subject).all()

        for subject in subjects:
            subject_summary = {
                'subject_name': subject.name,
                'quiz_count': 0,
                'pending': 0,
                'average_score': 0
            }

            chapters = subject.chapters

            all_quizzes = []
            for chapter in chapters:
                all_quizzes.extend(chapter.quizzes)

            quiz_count = len(all_quizzes)
            subject_summary['quiz_count'] = quiz_count

            quiz_ids = [quiz.id for quiz in all_quizzes]

            if quiz_ids:
                scores = (db.session.query(Score).filter(Score.quiz_id.in_(quiz_ids), Score.user_id == user_id).all())
            subject_summary['pending'] = quiz_count - len(scores)
            subject_summary['average_score'] = round(sum((s.total_scored or 0) for s in scores) / len(scores), 2) if scores else 0

            data.append(subject_summary)

        cache.set("user_summary_data", data, timeout=60)
        return data, 200

api.add_resource(AdminSummaryResource, '/api/admin/summary')
api.add_resource(UserSummaryResource, '/api/users/summary/<int:user_id>')
