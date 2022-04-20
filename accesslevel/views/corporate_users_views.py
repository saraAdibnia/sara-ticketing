from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from user.my_authentication.aseman_token_auth import MyToken
from accesslevel.models import CommonAccessLevel
from accesslevel.serializers import CommonAccessLevelSerializer
from accesslevel.permissions import CorporateUsersPermission
from user.models import User
from user.serializers import (
    UserShowSerializer,
    UserSerializer,
    # UserInfoSerializer,
)
from user.models.user import User
from extra_scripts import persian_calendar
from rest_framework.authtoken.models import Token
from re import sub
from extra_scripts.EMS import validation_error, existence_error
from extra_scripts import sum_cargo_list
from math import ceil
from pprint import pprint


class CorporateUsers(APIView):
    """helps to manage corporate user's access level"""

    permission_classes = [CorporateUsersPermission]

    def post(self, request):
        """list of corporate users"""
        allowed_filters = (
            "mobile__contains",
            "fname__contains",
            "flname__contains",
            "common_access_level__common_access_level_group",
        )
        kwargs = {}
        for key, value in request.data.items():
            if key in allowed_filters:
                kwargs.update({key: value})

        n = int(request.data.get("page", 1))
        items_per_page = int(request.data.get("items_per_page", 10))

        try:
            user_objs = (
                User.objects.filter(role=1)
                .filter(**kwargs)
                .order_by("-id")[items_per_page * (n - 1): items_per_page * (n)]
            )
        except IndexError:
            pass

        user_serialized = UserInfoSerializer(
            user_objs,
            many=True,
        )

        total_filtered = User.objects.filter(
            role=1).filter(**kwargs).count()
        pages = ceil(total_filtered / items_per_page)

        response_json = {
            "succeeded": True,
            "users": user_serialized.data,
            "total_filtered": total_filtered,
            "pages": pages,
        }

        return Response(response_json, status=200)

    def get(self, request):
        """details of a corporate user"""

        user_obj = User.objects.filter(
            id=request.query_params.get("id")).first()

        user_serialized = UserInfoSerializer(
            user_obj,
        )

        response_json = {"succeeded": True, "user": user_serialized.data}

        return Response(response_json, status=200)

    def patch(self, request):
        """make user ban or deactivate"""
        user_obj = User.objects.filter(
            id=request.data.get("id")).first()
        if not user_obj:
            return existence_error("user_obj")

        user_serialized = UserSerializer(
            user_obj,
            data={
                "is_active": request.data.get("is_active"),
                "banned": request.data.get("banned"),
                "banned_by": request.user.id,
            },
            partial=True,
        )
        if not user_serialized.is_valid():
            return validation_error(user_serialized)
        user_serialized.save()

        pass


class CorporateUsersActivity(APIView):


    def post(self, request):
        # get all user created by this co_user
        user_id = request.data.get('id')

        n = int(request.data.get("page", 1))
        items_per_page = int(request.data.get("items_per_page", 10))
        allowed_filters = (
            "created_time_gte",
            "created_time_lte",
        )
        kwargs = {}
        for key, value in request.data.items():
            if key in allowed_filters:
                kwargs.update({key: value})

        n = int(request.data.get("page", 1))
        items_per_page = int(request.data.get("items_per_page", 10))

        main_query = User.objects.filter(
            created_by=user_id)
        try:
            user_objs = (
                main_query.filter()  # TODO add kwargs later
                .filter(**kwargs,)
                .order_by("-id")[items_per_page * (n - 1): items_per_page * (n)]
            )
        except IndexError:
            pass

        user_serialized = UserInfoSerializer(
            user_objs,
            many=True,
        )
        total_filtered = user_objs.count()
        json_response = {
            "users_data": user_serialized.data,
            "total": main_query.count(),
            "total_filtered": total_filtered,
            "page": ceil(total_filtered / items_per_page)
        }
        return Response(json_response, status=200)
# For waybills

    def patch(self, request):  # return the nubmer of waybills created by a user, their nubmers and total mass_weight
        # in filter and non_filter request

        user_id = request.data.get('id')
        # check user existence
        if not User.objects.filter(id=user_id).exists():
            return existence_error("use object")

        allowed_filters = (
            "created_time_gte",
            "created_time_lte",
        )
        kwargs = {}
        for key, value in request.query_params.items():
            if key in allowed_filters:
                kwargs.update({key: value})
    # import query
        all_import_wbs = Waybill.objects.filter(
            created_by=user_id, deleted=False)
        # get all waybill and sum of cargo
        filtered_import_wbs = all_import_wbs.filter(**kwargs)
        all_filtered_import_cargo_sum = sum_cargo_list.get_sum_of_all_cargo(
            filtered_import_wbs)

        # get only submiited wbs and their cargo sum
        import_submitteds = filtered_import_wbs.filter(step__gte=5)

        # submitted_filtered_import_cargo_sum = sum_cargo_list.get_sum_of_all_cargo(
        #     import_submitteds)

    # export query
        all_export_wbs = ExportWaybill.objects.filter(
            created_by=user_id, deleted=False)
        # get all waybill and sum of cargo
        filtered_export_wbs = all_export_wbs.filter(**kwargs)
        all_filtered_export_cargo_sum = sum_cargo_list.get_sum_of_all_cargo(
            filtered_export_wbs)

        # get only submiited wbs and their cargo sum
        export_submitteds = filtered_export_wbs.filter(step__gte=5)

        # submitted_filtered_import_cargo_sum = sum_cargo_list.get_sum_of_all_cargo(
        #     export_submitteds)

        # CHART DATA
        ranges = persian_calendar.english_date_ranges(
            number_of_month=5)
        chart_data = []
        import_country_arr = []
        export_country_arr = []
        for range in ranges:  # filtering the w query based on the ranges
            import_wbs_in_month = all_import_wbs.filter(
                # range_1 is start and range_2 is end
                created__range=[range['range_1'], range['range_2']]
            )
            export_wbs_in_month = all_export_wbs.filter(
                # range_1 is start and range_2 is end
                created__range=[range['range_1'], range['range_2']]
            )
            internals = []

            chart_data.append(
                {
                    'month_number': range['persian_month'],
                    "number_imports": len(import_wbs_in_month),
                    "number_exports": len(export_wbs_in_month),
                    "number_internals": len(internals),
                }
            )

        json_respons = {
            #import data
            "total_import_number_filtered": len(filtered_import_wbs),
            "all_filtered_cargo_sum": all_filtered_import_cargo_sum,
            # export data
            "total_export__number_filtered": len(filtered_export_wbs),
            "all_filtered_export_cargo_sum": all_filtered_export_cargo_sum,

            "chart_data": chart_data,
        }

        return Response(json_respons, status=200)
