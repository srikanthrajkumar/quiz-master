from celery import Celery

celery = Celery(
    "quizmaster",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

def init_celery(app):
    celery.conf.update(app.config)