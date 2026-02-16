#!/bin/bash
set -e

echo "--- STARTING FRESH DEPLOYMENT SEQUENCE ---"

# 1. Fix Static Files
echo "Creating staticfiles directory..."
mkdir -p staticfiles
echo "Running collectstatic..."
python manage.py collectstatic --noinput

# 2. Reset Migrations
echo "Regenerating JobTech migrations..."
# Ensure the conflicting migration is gone (if it wasn't deleted by git)
rm -f JobTech/migrations/0001_initial.py
python manage.py makemigrations JobTech
python manage.py makemigrations

echo "Resetting Database History..."
# Force Django to forget it ever ran JobTech migrations
# We ignore errors here in case the app label is already reset or missing
python manage.py migrate --fake JobTech zero || true

echo "Applying Migrations..."
# This should now create the 'jobtech_job' table because of the fresh migration
python manage.py migrate

# 3. Start Server
echo "Starting Gunicorn..."
exec gunicorn Home.wsgi
