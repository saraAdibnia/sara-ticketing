from math import ceil
from developinglogs.serializers.sms_log_serializers import SMSLogShowSerializer
from rest_framework.views import APIView
from developinglogs.models import SMSLog
from developinglogs.serializers import SMSLogSerializer
from rest_framework.response import Response
from extra_scripts.send_sms import send_sms
import requests
from extra_scripts.EMS import existence_error, validation_error

from rest_framework.permissions import IsAuthenticated
from developinglogs.models.sms_log_models import SmsCategory
import datetime as dt
from icecream import ic

class SmsApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # list of all sms logs 

        # Filter result
        allowed_filters = (
            "code",
            "title__contains",
            "isActive",
            "sendByNumber__contains",
        )
        kwargs = {}
        for key, value in request.query_params.items():
            if key in allowed_filters:
                kwargs.update({key: value})

        n = int(request.query_params.get("page", 1))
        items_per_page = int(request.query_params.get("items_per_page", 10))

        # TODO : برای فیلدهای کزارشی مخصوصا فیلدهای تعدادی ، پایمک های دریافتی و ارسالی را از همدیگر مجزا نکرده ایم
        total_sms_cost = 0

        main_sms_logs = SMSLog.objects.filter(**kwargs, is_sending=True).all()
        total_sms_cost = sum([log.cost for log in main_sms_logs if log.cost ]) # calc sum cost of all sent sms

        # تعداد پیامک های در صف ارسال
        send_queue_count = main_sms_logs.filter(status=1).count()
        # تعداد پیامک های رسیده به گیرنده
        delivered_sms_count = main_sms_logs.filter(status=10).count()

        sms_logs = main_sms_logs.order_by(
            '-id')[items_per_page * (n - 1): items_per_page * (n)]
        sms_serialized = SMSLogShowSerializer(sms_logs, many=True)

        total_filtered = main_sms_logs.count()
        pages = ceil(total_filtered / items_per_page)

        response_json = {
            "suceeded": True,
            "send_queue_count": send_queue_count,
            "delivered_sms_count": delivered_sms_count,
            "total_sms_cost": total_sms_cost,
            "sms_logs": sms_serialized.data,
            "total_filtered": total_filtered,
            "pages": pages,
        }

        return Response(response_json, status=200)

    def post(self, request):
        kwargs = {}
        if request.data.get('date_time'):
            send_time = dt.datetime.strptime(
                request.data.get('date_time'), '%Y-%m-%dT%H:%M:%S.%fZ')
            kwargs.update({'eta': send_time})

        smsCategory_obj = SmsCategory.objects.filter(code=15).first()
        if smsCategory_obj.isActive == True:
            sms_text = request.data.get("message")
            # send_sms.apply_async((
            send_sms(
                request.data.get("receptor"),
                sms_text,
                smsCategory_obj.id,
                smsCategory_obj.get_sendByNumber_display(),
                request.user.id,)
            # ), priority=10, **kwargs)

        response_json = {
            "suceeded": True,
        }
        return Response(response_json, status=200)

    def patch(self, request):

        sms = request.data.get("sms")

        sms_log = SMSLog.objects.filter(id=sms).first()
        sms_serialized = SMSLogShowSerializer(sms_log)

        response_json = {
            "succeeded": True,
            "sms": sms_serialized.data,
        }

        return Response(response_json, 200)


class SmsReportView(APIView):
    def get(self, request):
        info_url = "https://api.kavenegar.com/v1/58546C51517035384E664B44345970343258654E2F5132383555714C69437876616358682B6B444E777A673D/account/info.json"
        info_response = requests.get(url=info_url)
        # status =1 # تعداد پیامک های در صف ارسال
        # kave_send_count = f"https://api.kavenegar.com/v1/58546C51517035384E664B44345970343258654E2F5132383555714C69437876616358682B6B444E777A673D/sms/countoutbox.json?startdate={start_date}&enddate={end_date}&status={status}"
        response_json = {
            "succeeded": True,
            "info": info_response.json(),
        }
        return Response(response_json, status=200)


class SMSRecieveView(APIView):

    def patch(self, request):  # get a smslog using id
        smslog_object = SMSLog.objects.filter(
            id=request.data.get('sms_id')).first()  # handle the exist error
        if not smslog_object:
            return existence_error('smslog_object')
        serialized_data = SMSLogSerializer(smslog_object)
        return Response({"sms_data": serialized_data.data}, status=200)

    def get(self, request):  # get all the is_sending smslogs with and without filtering

        n = int(request.query_params.get("page", 1))
        items_per_page = int(request.query_params.get("items_per_page", 10))

        allowed_filters = (
            "sender",
            "message__contains",
            "start_date",
            "end_date",
            "created_date__gte",
            "created_date__lte",
        )

        kwargs = {}
        for key, value in request.query_params.items():
            if key in allowed_filters:
                kwargs.update({key: value})

        main_query = SMSLog.objects.filter(is_sending=False).all()
        smslogs = main_query.filter(
            **kwargs).order_by('-id')[items_per_page * (n - 1): items_per_page * (n)]
        serialized_data = SMSLogSerializer(smslogs, many=True)
        total_filtered = smslogs.count()
        pages = ceil(total_filtered / items_per_page)
        total = main_query.count()

        json_response = {
            "data": serialized_data.data,
            "total_filtered": total_filtered,
            "total": total,
            "pages": pages,
        }
        return Response(json_response, status=200)

