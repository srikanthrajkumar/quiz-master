from flask_restful import Api

api = Api()

def init_api(app):
    from . import users, subjects, chapters, quizzes, questions, scores
    api.init_app(app)
