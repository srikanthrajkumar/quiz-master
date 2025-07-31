# Quiz Master - V2

A full-stack quiz management platform built with Flask, Vue.js, SQLite, Redis, and Celery. Users can register, attempt quizzes, view scores, and download reports. Admins can manage subjects, chapters, quizzes, and questions, with full analytics and background task support.

---

## Project Structure

├── run.py # Entry point to run the Flask app
├── auth.py # Auth-related helper functions
├── requirements.txt # Python dependencies
├── backend/
│ └── app/
│ ├── init.py # App factory and configuration
│ ├── api/ # Route controllers
│ ├── models.py # SQLAlchemy models
│ ├── jobs.py # Celery background jobs
│ ├── celery_entry.py # Celery app entrypoint
│ ├── templates/ # Flask-rendered templates
│ ├── static/ # Static files for Flask routes
├── frontend/
│ ├── src/ # Vue.js source code (components, pages, services)
│ ├── public/ # Static files served by Vite
│ ├── vite.config.js # Vite configuration
├── instance/
│ ├── quizmaster.db # SQLite database file
│ └── exports/ # Exported CSV files
├── migrations/ # Alembic database migrations
└── venv/ # Python virtual environment

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Celery
- **Frontend**: Vue.js, Vite, Axios
- **Database**: SQLite (dev) with Alembic for migrations
- **Broker**: Redis (for background tasks)

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/21f3001497/quiz-master-v2
cd quiz-master
```
### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
python -m venv venv
source venv/bin/activate
```
### 4. Install Node Dependencies (Frontend)
```bash
cd frontend
npm install
cd ..
```

## Running the Project

Use three terminals (in the root directory):

### Terminal 1: Flask App
```bash
source venv/bin/activate
python run.py
```

### Terminal 2: Frontend App
```bash
source venv/bin/activate
cd frontend
npm run dev
```

### Terminal 2: Frontend App
```bash
source venv/bin/activate
celery -A backend.app.celery_entry.celery worker --loglevel=info
```

Make sure Redis is running before starting the Celery worker:
```bash
redis-server
```