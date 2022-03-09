from math import ceil
from re import sub

from rest_framework.authtoken.models import Token
from developinglogs.serializers.sms_log_serializers import SmsCategorySerializer
from developinglogs.models.sms_log_models import SmsCategory
from rest_framework.views import APIView
from extra_scripts.EMS import existence_error, validation_error
from django.utils import timezone
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated


class SmsManageView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """get all SmsCategory"""

        # Filter result
        allowed_filters = (
            "code",
            "title__contains",
            "isActive",
            "sendByNumber__contains",
            "kind",
        )
        kwargs = {}
        for key, value in request.query_params.items():
            if key in allowed_filters:
                kwargs.update({key: value})

        # Pagination
        n = int(request.query_params.get("page", 1))
        print(n*12)
        items_per_page = int(request.query_params.get("items_per_page", 10))

        mainSmsCategory_objs = SmsCategory.objects.filter(**kwargs)

        smsCategory_obj = mainSmsCategory_objs.order_by("-id")[
            items_per_page * (n - 1): items_per_page * (n)
        ]
        try:

            smsCategorySerialized = SmsCategorySerializer(
                smsCategory_obj,
                many=True,
            )
        except IndexError:
            return existence_error(smsCategory_obj)

        total_filtered = len(mainSmsCategory_objs)
        pages = ceil(total_filtered / items_per_page)

        response_json = {
            "succeeded": True,
            "smsCat_objs": smsCategorySerialized.data,
            "total_filtered": total_filtered,
            "pages": pages,
            "numbers": SmsCategory._meta.get_field("sendByNumber").choices,
        }

        return Response(response_json, status=200)

    def post(self, request):
        """add new sms category"""
        request.data.update({'activeBy': request.user.id})
        smsCategory_serialized = SmsCategorySerializer(data=request.data)
        if not smsCategory_serialized.is_valid():
            return validation_error(smsCategory_serialized)
        smsCategory_serialized.save()

        response_json = {"succeeded": True}

        return Response(response_json, status=200)

    def patch(self, request):
        """update the smscategory"""
        smsCat_id = request.data.get("id")
        isActive = request.data.get("isActive", True)
        smsText = request.data.get("smsText")
        sendByNumber = request.data.get("sendByNumber")

        smsCat_obj = SmsCategory.objects.filter(id=smsCat_id).last()

        smsCategory_serialized = SmsCategorySerializer(
            smsCat_obj,
            data={
                "isActive": isActive,
                "activeBy": request.user.id,
                "modified": timezone.now(),
                "smsText": smsText,
                'sendByNumber': sendByNumber,

            },
            partial=True,
        )

        if not smsCategory_serialized.is_valid():
            return validation_error(smsCategory_serialized)
        smsCategory_serialized.save()

        response_json = {"succeeded": True}

        return Response(response_json, status=200)
