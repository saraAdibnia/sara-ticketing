from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from rest_framework.response import Response


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TicketingSystem.settings')
app = Celery('TicketingSystem')


app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')