from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime as dt
from rest_framework import generics
from accesslevel.serializers import (
    UserRowCountAccessSerializer, UserRowCountAccessCreateSerializer)

from accesslevel.models import (
    UserRowCountAccess, )
from django.apps import apps
from extra_scripts.EMS import (
    validation_error, )
from math import ceil
from django.apps import apps as total_apps


class UserRowCountAccessViews(APIView):

    def get(self, request):
        # get the list of model
        allowed_filters = (
            "model_name__contains",
            "role__id",
            "title__contains",
        )
        
        kwargs = {}
        for key, value in request.query_params.items():
            if key in allowed_filters:
                kwargs.update({key: value})

        n = int(request.query_params.get("page", 1))
        items_per_page = int(request.query_params.get("items_per_page", 10))
        queryset = UserRowCountAccess.objects.all()
        qs = queryset.filter(**kwargs)
        ser = UserRowCountAccessSerializer(qs.order_by(
            "-id")[items_per_page * (n - 1): items_per_page * (n)], many=True)
        # send all of the model names to front
        # models = [m.__name__ for m in apps.get_app_config(
            # 'order').get_models()]  # get models in order

        models = [m.__name__ for m in apps.get_models()] # get all models in projects

        jr = {
            "total": len(queryset),
            "total_filtered": len(qs),
            "user_row_count_access": ser.data,
            "pages": ceil(len(queryset) / items_per_page),
            "items_per_page": items_per_page,
            "db_models": models
        }
        return Response(jr, status=200)

    def patch(self, request):
        # get one object detail
        obj = UserRowCountAccess.objects.get(id=request.query_params.get('id'))
        ser = UserRowCountAccessSerializer(obj)
        return Response(ser.data, status=200)

    def post(self, request):
        # create one user_row_count_access object
        ser = UserRowCountAccessCreateSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
        else:
            return validation_error(ser)
        jr = {
            'succeeded': True,
            'data': ser.data
        }
        return Response(jr, status=200)

    def put(self, request):
        # create one user_row_count_access object
        obj = UserRowCountAccess.objects.get(id=request.query_params.get('id'))
        ser = UserRowCountAccessCreateSerializer(
            instance=obj,  data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
        else:
            return validation_error(ser)
        jr = {
            'succeeded': True,
            'data': ser.data
        }

        return Response(jr, status=200)




