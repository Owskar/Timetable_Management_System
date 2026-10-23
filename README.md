# Timetable Management System

A Django-based timetable management application. The repository includes Django project code, templates, static assets, and a SQLite database file.

## Requirements

- Python
- Dependencies listed in `requirements.txt`

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

On macOS or Linux, activate the environment with `source .venv/bin/activate`. Open the local URL printed by Django in your browser. Review the project settings before deploying.