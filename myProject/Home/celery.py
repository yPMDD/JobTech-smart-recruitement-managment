# myproject/celery.py
from celery import Celery
from datetime import datetime, timedelta
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Home.settings')

app = Celery('Home')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Schedule periodic tasks (optional)
app.conf.beat_schedule = {
    'send-scheduled-emails': {
        'task': 'Home.tasks.send_scheduled_emails',
        'schedule': 60.0,  # Check every 60 seconds
    },
}