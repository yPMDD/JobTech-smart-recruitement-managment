# myapp/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime

@shared_task
def send_scheduled_email(subject, message, recipient, send_at):
    from datetime import datetime
    now = datetime.now()
    if now >= send_at:
        send_mail(
            subject=subject,
            message=message,
            from_email="saad989011@gmail.com",
            recipient_list=[recipient],
        )
    else:
        # Re-schedule if not yet time
        send_scheduled_email.apply_async(
            args=[subject, message, recipient, send_at],
            eta=send_at,  # Execute at this exact time
        )