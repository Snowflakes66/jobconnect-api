# JobConnect API

A Django REST API for job posting and applications built with Django REST Framework.

## Features
- User registration and token authentication
- Employers can post, edit and delete jobs
- Job seekers can browse jobs and submit applications
- Application status tracking (pending, accepted, rejected)
- Secure token-based authentication on all protected endpoints

## Tech Stack
- Python
- Django
- Django REST Framework
- SQLite
- Token Authentication

## Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register/ | Register a new user |
| POST | /api/auth/login/ | Login and get token |
| POST | /api/auth/logout/ | Logout |
| GET | /api/auth/profile/ | View your profile |
| GET | /api/jobs/ | List all active jobs |
| POST | /api/jobs/ | Post a new job |
| GET | /api/jobs/<id>/ | View a single job |
| PUT | /api/jobs/<id>/ | Update a job |
| DELETE | /api/jobs/<id>/ | Delete a job |
| POST | /api/jobs/<id>/apply/ | Apply for a job |
| GET | /api/applications/ | View your applications |
| GET | /api/my-jobs/ | View jobs you posted |

## Setup
```bash
git clone https://github.com/Snowflakes66/jobconnect-api.git
cd jobconnect-api
python -m venv venv
venv\Scripts\activate
pip install django djangorestframework
python manage.py migrate
python manage.py runserver
```

## Author
Ayomide — Python/Django Backend Developer
ALX Africa Certified