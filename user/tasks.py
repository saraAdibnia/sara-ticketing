from celery import shared_task
from pprint import pprint
from user.models import User
from extra_scripts.send_sms import send_sms
from developinglogs.models.sms_log_models import SmsCategory
import datetime
from persiantools.jdatetime import JalaliDate
from System.models import *


@shared_task(name = 'add')
def add(x, y):
    z = x + y
    return z




# @shared_task(name='send_hbd_sms')
# def send_hbd_sms():
#     persian_month = JalaliDate(datetime.date.today()).month
#     persian_day = JalaliDate(datetime.date.today()).day
#     users = [person for person in User.objects.filter(birthday__month=persian_month, birthday__day=persian_day).all()
#              if person.birthday]
#     print(f'number of users are ************ {len(users)}')

#     smsCategory_obj = SmsCategory.objects.filter(code=16).first()
#     print(f'the id is {smsCategory_obj.id} \n\n\n')
#     sms_text = smsCategory_obj.smsText
#     if smsCategory_obj.isActive == True:
#         for user in users:
#             send_sms(
#                 user.mobile,
#                 sms_text.format(user.fname, user.flname),
#                 smsCategory_obj.id,
#                 smsCategory_obj.get_sendByNumber_display(),
#             )

#     result = "all the message for HBD was sent to users"
#     return result

