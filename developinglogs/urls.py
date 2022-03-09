from django.urls import path

from developinglogs.views import *


urlpatterns = [
    path("sms_delivery/", SMSDeliveryCallBack.as_view()),
    path("send_sms/", SmsApiView.as_view()),
    path("sms_sent/", SmsSentView.as_view()),
    path("sms_manage/", SmsManageView.as_view()),
    path("sms_report/", SmsReportView.as_view()),
    path("sms_recieve_view/", SMSRecieveView.as_view()),
    path("ReceiveSMS/", ReceivedSmsViews.as_view()),

]
