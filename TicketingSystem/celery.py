from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from rest_framework.response import Response
from icecream import ic
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TicketingSystem.settings')
app = Celery('TicketingSystem')


app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'user.tasks.add',
        'schedule':crontab(minute='*/1'),
        'args': (16, 16)
    },
}
# app.conf.timezone = 'Iran'