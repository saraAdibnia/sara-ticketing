# from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from rest_framework.response import Response
from icecream import ic
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TicketingSystem.settings')
app = Celery('TicketingSystem')

app.config_from_object('django.conf:settings' , namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# CELERY_IMPORTS = ("user.tasks", )

from celery.schedules import crontab


app.conf.beat_schedule = {
    'add-every-30-seconds-by-ruhy': {
        'task': 'add',
        'schedule':30.0,
        'args': (16, 16),
    },
     'suspend-every-Sunday': {
        'task': 'to_suspend',
        'schedule':crontab(day_of_week='Sunday')
    },
}
# app.conf.timezone = 'Iran'