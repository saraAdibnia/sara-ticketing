from celery import shared_task
from pprint import pprint
from user.models import User
from extra_scripts.send_sms import send_sms
from developinglogs.models.sms_log_models import SmsCategory
import datetime
from persiantools.jdatetime import JalaliDate
from System.models import *
from icecream import ic



@shared_task(name = 'add')
def add(x, y):
    z = x + y
    ic('testting the celery app')
    return z*10
