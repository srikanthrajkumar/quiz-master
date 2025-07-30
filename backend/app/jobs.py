import os
import csv
from .celery_app import celery

@celery.task(bind=True)
def export_scores_to_csv(self, user_id):
    from flask import Flask
    from . import db
    from .models import Score
    
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'quizmaster.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    os.makedirs(app.instance_path, exist_ok=True)
    
    db.init_app(app)
    
    with app.app_context():
        scores = Score.query.filter_by(user_id=user_id).all()
        
        directory = os.path.join(app.instance_path, 'exports')
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, f'{user_id}.csv')
        
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Score ID', 'Quiz ID', 'Time Stamp', 'Score'])
            for score in scores:
                writer.writerow([score.id, score.quiz_id, score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S') if score.time_stamp_of_attempt else '', score.total_scored])
        
        return path