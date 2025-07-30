import os
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.jobs import export_scores_to_csv
from backend.app.celery_app import celery
from . import api

class ExportScoresResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        job = export_scores_to_csv.delay(user_id)
        return {"job_id": job.id}, 202

class ExportStatusResource(Resource):
    @jwt_required()
    def get(self, job_id):
        job = celery.AsyncResult(job_id)
        if job.state == 'PENDING':
            return {"status": "processing"}, 200
        elif job.state == 'SUCCESS':
            file_path = job.result
            filename = os.path.basename(file_path)
            download_url = f"/downloads/{filename}"
            return {"status": "completed", "download_url": download_url}, 200
        else:
            return {"status": "failed", "error": str(job.info)}, 500

api.add_resource(ExportScoresResource, '/api/export_csv')
api.add_resource(ExportStatusResource, '/api/export_status/<job_id>')