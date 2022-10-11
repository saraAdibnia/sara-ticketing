from django.shortcuts import render
from .models import User_log
from math import ceil
from . serializers import UserLogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from extra_scripts.EMS import existence_error

# from accesslevel.permissions import CorporateUsersPermission


class UserLogView(APIView):

    # permission_classes = [CorporateUsersPermission]

    def get(self, request):  # get all user_logs based on thier id and date period
        allowed_filters = (
            "user__id",
            "date__gte",
            "date__lte",
            "log_kind",
            "user__fname__contains",
            "user__mobile__contains",
            "user__flname__contains",
            "ip_address__contains",
            "user__role",
            "user__is_active",
        )
        kwargs = {}
        for key, value in request.query_params.items():
            if key in allowed_filters:
                kwargs.update({key: value})

        n = int(request.query_params.get("page", 1))
        items_per_page = int(request.query_params.get("items_per_page", 10))

        main_query = User_log.objects.filter(**kwargs).all()
        # if not main_query.exists():
        #     return existence_error("user")
        user_logs = main_query.order_by(
            '-id')[items_per_page * (n - 1): items_per_page * (n)]

        total_filtered = len(main_query)

        serialized_data = UserLogSerializer(user_logs, many=True).data

        response_json = {
            "total_filtered": total_filtered,
            "pages": ceil(total_filtered / items_per_page),
            "data": serialized_data,
        }

        return Response(response_json, status=200)

    def patch(self, request):
        # get all logs of given user
        user_id = request.data.get('user_id')
        allowed_filters = (
            "date__gte",
            "date__lte",
            "log_kind",
            "ip_address__contains",
        )
        kwargs = {}
        for key, value in request.data.items():
            if key in allowed_filters:
                kwargs.update({key: value})

        main_query = User_log.objects.filter(user__id=user_id).all()

        n = int(request.data.get("page", 1))
        items_per_page = int(request.data.get("items_per_page", 10))

        filtered_query = main_query.filter(**kwargs).all()

        if not filtered_query.exists():
            return existence_error("user_log")

        user_logs = filtered_query.order_by(
            '-id')[items_per_page * (n - 1): items_per_page * (n)]

        total_filtered = len(filtered_query)
        serialized_data = UserLogSerializer(user_logs, many=True).data

        response_json = {
            "total_filtered": total_filtered,
            "pages": ceil(total_filtered / items_per_page),
            "data": serialized_data,
        }

        return Response(response_json, status=200)
