#!/bin/bash
set -e

echo "--- STARTING FRESH DEPLOYMENT SEQUENCE ---"

# 1. Fix Static Files
echo "Creating staticfiles directory..."
mkdir -p staticfiles
echo "Running collectstatic..."
python manage.py collectstatic --noinput

# 2. Database Migrations
echo "Applying migrations..."
python manage.py makemigrations jobtech
python manage.py makemigrations users
python manage.py migrate


# 3. Start Server
echo "Starting Gunicorn..."
exec gunicorn Home.wsgi
