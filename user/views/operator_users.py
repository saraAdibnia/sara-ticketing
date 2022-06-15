
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from extra_scripts.EMS import *
from math import ceil
from utilities.pagination import CustomPagination
from user.serializers.user_serializers import UserProfileQuickSerilaizer, UserSerializer, UserSimpleSerializer 
from rest_framework import generics, filters


class CorportateUsers(APIView):
    #
    # permission_classes = [IsAuthenticated]

    def get(self, request):

        allowed_filters = (
            "created_time_gte",
            "created_time_lte",
        )
        kwargs = {}
        for key, value in request.query_params.items():
            if key in allowed_filters:
                kwargs.update({key: value})

        n = int(request.query_params.get("page", 1))
        items_per_page = int(request.query_params.get("items_per_page", 10))
        corp_user = User.objects.filter(id=request.GET['id']).first()
        if not corp_user:
            return existence_error(corp_user)
        users = User.objects.filter(created_by=corp_user, **kwargs)
        filtered_uss = users.filter().order_by(
            "-id")[items_per_page * (n - 1): items_per_page * (n)]
        serialized = UserSerializer(users, many=True)
        # for person in serialized.data:  # send last order of user
        #     person.update({
        #         'last_import_waybill_order':  WaybillSerializerStepOne(Waybill.objects.filter(user=person['id']).last()).data
        #     })

        json_res = {"users": serialized.data,
                    "total_filtered": len(users),
                    "page": ceil(len(users) / items_per_page),

                    }
        return Response(json_res, status=200)


class StaffListView(APIView):
    #pagination_class = CustomPagination()
    def get(self, request):
        users = User.objects.filter(role = 1)
        page = self.pagination_class.paginate_queryset(queryset = users ,request =request)
        serializer = UserSimpleSerializer(page , many=True)
        return self.pagination_class.get_paginated_response(serializer.data)
    
class UserNormalSearch(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSimpleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ("id", "mobile__icontains", "fname__icontains",
                    "flname__icontains", "ename__icontains")
    
