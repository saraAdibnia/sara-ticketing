from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from rest_framework.response import Response
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TicketingSystem.settings')
app = Celery('TicketingSystem')


app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=17, minute=0, day_of_week=3),
         'args': (16, 16)
    },
}
@app.task(bind=True)
def add(x, y):
    z = x + y
    print(z)