# Quiz Master - V2

A full-stack quiz management platform built with Flask, Vue.js, SQLite, Redis, and Celery. 

---

## Project Structure

```text
├── run.py
├── auth.py
├── requirements.txt
├── backend/
│   └── app/
│       ├── __init__.py
│       ├── api/
│       ├── models.py
│       ├── jobs.py
│       ├── celery_entry.py
│       ├── templates/
│       └── static/
├── frontend/
│   ├── src/               # Vue.js source code (components, pages, services)
│   ├── public/            
│   └── vite.config.js 
├── instance/
│   ├── quizmaster.db 
│   └── exports/
├── migrations/
└── venv/
```

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Celery
- **Frontend**: Vue.js, Vite, Axios
- **Database**: SQLite (dev) with Alembic for migrations
- **Broker**: Redis (for background tasks)

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/21f3001497/quiz-master-v2.git
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
