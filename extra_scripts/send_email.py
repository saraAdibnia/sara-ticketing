from user.models import User
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from datetime import datetime

@shared_task
def send_email(subject, body, receiver_address):
    # user = User.objects.get(id = user_id)
    send_mail(subject, body, settings.EMAIL_HOST_USER,
              [receiver_address], fail_silently=False)
    return 'email has been sent'
