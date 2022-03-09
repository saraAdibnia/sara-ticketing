from developinglogs.serializers.sms_log_serializers import SMSLogSerializer
from rest_framework.views import APIView
from developinglogs.models import SMSLog
from math import ceil
from extra_scripts.EMS import existence_error
from rest_framework.response import Response


class SmsSentView(APIView):
    def get(self, request):
        """get all sent sms , can filter by consignee, number and kind of sms"""

        #### Filter result
        allowed_filters = ("kind", "status", "sender", "receptor", "date")
        kwargs = {}
        for key, value in request.data.items():
            if key in allowed_filters:
                kwargs.update({key: value})
        ### Pagination
        n = int(request.data.get("page", 1))
        items_per_page = int(request.data.get("items_per_page", 10))

        mainSms_objs = SMSLog.objects.all().filter(**kwargs)

        try:
            sms_obj = mainSms_objs.order_by("-id")[
                (n - 1) * items_per_page : (n * items_per_page) - 1
            ]

            sms_serialized = SMSLogSerializer(sms_obj, many=True)
        except IndexError:
            return existence_error(sms_obj)

        total_filtered = len(mainSms_objs)
        pages = ceil(total_filtered / items_per_page)
        total_cost = 0.0
        total_delivered = 0
        for item in mainSms_objs:
            total_cost += item.cost
            if item.status == 10:
                total_delivered += 1

        response_json = {
            "succeeded": True,
            "sms_objs": sms_serialized.data,
            "total_filtered": total_filtered,
            "pages": pages,
            "total_cost": total_cost,
            "total_delivered": total_delivered,
        }

        return Response(response_json, status=200)
