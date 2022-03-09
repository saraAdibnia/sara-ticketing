
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import UserProfile
from extra_scripts.EMS import *
from math import ceil
# from user.serializers import UserProfileInfoSerializer

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
        corp_user = UserProfile.objects.filter(id=request.GET['id']).first()
        if not corp_user:
            return existence_error(corp_user)
        users = UserProfile.objects.filter(created_by=corp_user, **kwargs)
        filtered_uss = users.filter().order_by(
            "-id")[items_per_page * (n - 1): items_per_page * (n)]
        serialized = UserProfileInfoSerializer(users, many=True)
        # for person in serialized.data:  # send last order of user
        #     person.update({
        #         'last_import_waybill_order':  WaybillSerializerStepOne(Waybill.objects.filter(user=person['id']).last()).data
        #     })

        json_res = {"users": serialized.data,
                    "total_filtered": len(users),
                    "page": ceil(len(users) / items_per_page),

                    }
        return Response(json_res, status=200)
