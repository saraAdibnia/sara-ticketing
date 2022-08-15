# from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from rest_framework.response import Response
from icecream import ic
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TicketingSystem.settings')
app = Celery('TicketingSystem')

app.config_from_object('django.conf:settings' , namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from celery.schedules import crontab


app.conf.beat_schedule = {
    'add-every-minute': {
        'task': 'add',
        'schedule':crontab(minute='*/1'),
        'args': (16, 16),
    },
    #  'suspend-every-minute': {
    #     'task': 'System.tasks.to_suspend',
    #     'schedule':crontab(minute='*/1'),
    # },
}
# app.conf.timezone = 'Iran'