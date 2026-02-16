#!/bin/bash
set -e

echo "--- STARTING FRESH DEPLOYMENT SEQUENCE ---"

# 1. Fix Static Files
echo "Creating staticfiles directory..."
mkdir -p staticfiles
echo "Running collectstatic..."
python manage.py collectstatic --noinput

# 2. Database Migrations
echo "Applying migrations (with --fake-initial)..."
python manage.py migrate --fake-initial



# 3. Start Server
echo "Starting Gunicorn on port ${PORT:-8000}..."
exec gunicorn Home.wsgi --bind 0.0.0.0:${PORT:-8000} --timeout 120 --workers 2
