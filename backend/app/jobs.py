import os
import csv
import requests
import smtplib
from datetime import datetime
from flask import Blueprint
from celery.schedules import crontab
from .celery_app import celery
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template
from weasyprint import HTML

reminder_bp = Blueprint('reminder', __name__)
report_bp = Blueprint('report', __name__)

@celery.task()
def export_scores_to_csv(user_id):
    from .models import Score
    from flask import current_app
    
    scores = Score.query.filter_by(user_id=user_id).all()
    
    directory = os.path.join(current_app.instance_path, 'exports')
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f'{user_id}.csv')
    
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Score ID', 'Quiz ID', 'Time Stamp', 'Score'])
        for score in scores:
            writer.writerow([
                score.id, 
                score.quiz_id, 
                score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S') if score.time_stamp_of_attempt else '', 
                score.total_scored
            ])
    
    return path


@celery.task()
def daily_reminder():
    from .models import User, Score

    webhook_url = "https://chat.googleapis.com/v1/spaces/AAQAjHtz9vc/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=TRVFA6UKJ1I4hxAfOSEMvFqu_TzfV9EGRtJlfn-KZqo"
    
    users = User.query.all()
    today = datetime.now().date()
    
    for user in users:
        recent_score = (
            Score.query.filter_by(user_id=user.id)
            .order_by(Score.time_stamp_of_attempt.desc())
            .first()
        )
        if not recent_score or recent_score.time_stamp_of_attempt.date() != today:
            message = {
                'text': f"Hi {user.first_name}, don't forget to attempt a quiz today!"
            }
            try:
                requests.post(webhook_url, json=message)
            except requests.exceptions.RequestException as e:
                print(f"Failed to send reminder to {user.first_name}: {e}")

@celery.task()
def monthly_report():
    from flask import current_app
    from .models import User, Score, Quiz, Chapter

    users = User.query.all()
    scores = Score.query.all()
    quizzes = Quiz.query.all()
    chapters = Chapter.query.all()

    template_path = os.path.join(current_app.root_path, 'templates', 'monthly.html')
    with open(template_path) as file:
        template = Template(file.read())
        now = datetime.now()
        html_string = template.render(users=users, scores=scores, quizzes=quizzes, chapters=chapters, now=now)

    output_dir = os.path.join(current_app.root_path, 'static', 'pdf')
    os.makedirs(output_dir, exist_ok=True)
    pdf_filename = os.path.join(output_dir, f'monthly_report_{datetime.now().strftime("%Y-%m-%d")}.pdf')

    HTML(string=html_string).write_pdf(pdf_filename)

    msg = MIMEMultipart()
    msg['From'] = current_app.config['SMTP_SERVER_EMAIL']
    msg['To'] = 'srikanthrajkumar.iitm@gmail.com'
    msg['Subject'] = 'Monthly Quiz Master Report'
    msg.attach(MIMEText(html_string, 'html'))

    with open(pdf_filename, 'rb') as f:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_filename))
        msg.attach(attachment)

    server = smtplib.SMTP(
        host=current_app.config['SMTP_SERVER_HOST'],
        port=current_app.config['SMTP_SERVER_PORT']
    )
    server.starttls()
    server.login(
        current_app.config['SMTP_SERVER_EMAIL'],
        current_app.config['SMTP_SERVER_PASSWORD']
    )
    server.send_message(msg)
    server.quit()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=19, minute=0, day_of_week='*'),
        daily_reminder.s()
    )
    sender.add_periodic_task(
        crontab(hour=8, minute=0, day_of_month='1'),
        monthly_report.s()
    )


#For Testing purposes only
@reminder_bp.route('/daily_reminder', methods=['GET'])
def daily_reminder_route():
    job = daily_reminder.delay()
    return {'jobId': job.id}

#For Testing purposes only
@report_bp.route('/monthly_report', methods=['GET'])
def monthly_report_route():
    job = monthly_report.delay()
    return {'jobId': job.id}