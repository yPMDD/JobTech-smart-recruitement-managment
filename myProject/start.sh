#!/bin/bash
set -e

echo "--- STARTING FRESH DEPLOYMENT SEQUENCE ---"

# 1. Fix Static Files
echo "Creating staticfiles directory..."
mkdir -p staticfiles
echo "Running collectstatic..."
python manage.py collectstatic --noinput

# 2. Reset Migrations
echo "Regenerating migrations..."
python manage.py makemigrations jobtech
python manage.py makemigrations users
python manage.py makemigrations

echo "Resetting Database History..."
# Force Django to forget previous migrations for these apps
python manage.py migrate --fake jobtech zero || true
python manage.py migrate --fake users zero || true

echo "Applying Migrations..."
# This will now create the tables from scratch in the database if they don't exist
# or synchronize them if they do.
python manage.py migrate

# 3. Start Server
echo "Starting Gunicorn..."
exec gunicorn Home.wsgi

