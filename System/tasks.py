# from celery import shared_task
# from System.models import Ticket
# @shared_task(name='to_suspend')
# def to_suspend():
#     tickets = [ticket for ticket in Ticket.objects.filter(status=0).all()]
#     for ticket in tickets :
#         ticket.status = 3
#     return tickets


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

