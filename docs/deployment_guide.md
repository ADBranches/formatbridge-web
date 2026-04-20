# FormatBridge Deployment Guide

## Overview
FormatBridge MVP deployment includes:
- React frontend
- Flask backend
- Celery worker
- Redis
- PostgreSQL
- Nginx reverse proxy

## Recommended Services
- `frontend`
- `backend`
- `celery_worker`
- `redis`
- `postgres`
- `nginx`

## Environment
Use a production `.env` with:
- strong `SECRET_KEY`
- production database credentials
- production Redis URL
- production CORS origins
- cleanup retention values
- logging level

## Gunicorn
Run Flask with Gunicorn in production, not the development server.

Example:
```bash
gunicorn -w 3 -b 0.0.0.0:5000 wsgi:app
