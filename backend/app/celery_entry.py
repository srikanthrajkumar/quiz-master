from .celery_app import celery, init_celery
from . import create_app

app = create_app()
init_celery(app)

from . import jobs