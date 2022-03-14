# in this file we have apis that help to manage and view common access level stuff
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from user.models import UserProfile
from accesslevel.models import (
    CommonAccessLevel,
    CommonAccessLevelGroup,
)
from accesslevel.serializers import (
    CommonAccessLevelSerializer,
    CommonAccessLevelShowSerializer,
    CommonAccessLevelGroupSerializer,
)
from accesslevel.permissions import (
    CommonAccessLevelManagementPermission,
    AccessLevelTreePermission,
)
from extra_scripts.EMS import validation_error, existence_error


class CommonAccessLevelShowView(APIView):
    """helps to retreive common access level groups and itself."""

    permission_classes = [AccessLevelTreePermission]

    def get(self, request):
        """you can retreive every common access level groups that exist in the webservice"""
        # query for all common access level groups
        common_access_level_group_objs = CommonAccessLevelGroup.objects.all().order_by(
            "-id"
        )

        # serializing data
        common_access_level_group_serialized = CommonAccessLevelGroupSerializer(
            common_access_level_group_objs, many=True
        )

        response_json = {
            "succeeded": True,
            "common_access_level_groups": common_access_level_group_serialized.data,
        }

        return Response(response_json, status=200)

    def post(self, request):
        """you can retreive every common access level in a certain common access level group"""

        # query for cal in a certain cal group

        allowed_filters = ('common_access_level_group', )
        kwargs = {}
        for key, value in request.data.items():
            if key in allowed_filters:
                kwargs.update({key: value})

        common_access_level_objs = CommonAccessLevel.objects.filter(
            **kwargs).order_by("-id")

        common_access_level_serialized = CommonAccessLevelShowSerializer(
            common_access_level_objs, many=True
        )

        response_json = {
            "succeeded": True,
            "common_access_levels": common_access_level_serialized.data,
        }

        return Response(response_json, status=200)

    def patch(self, request):
        """you can send a common access level id and retrieve it's detailed informantion"""

        common_access_level_obj = CommonAccessLevel.objects.filter(
            id=request.data.get("id")
        ).first()

        common_access_level_serialized = CommonAccessLevelShowSerializer(
            common_access_level_obj
        )

        response_json = {
            "succeeded": True,
            "common_access_level": common_access_level_serialized.data,
        }
        return Response(response_json, status=200)


class CommonAccessLevelGroupManagementView(APIView):
    """helps to manage common access level groups"""

    permission_classes = [CommonAccessLevelManagementPermission]

    def get(self, request):
        """show group"""

        common_access_level_group_objs = CommonAccessLevelGroup.objects.all().order_by(
            "-id"
        )

        common_access_level_group_serialized = CommonAccessLevelGroupSerializer(
            common_access_level_group_objs, many=True
        )
        response_json = {
            "succeeded": True,
            "common_access_level_groups": common_access_level_group_serialized.data,
        }

        return Response(response_json, status=200)

    def post(self, request):
        """create group"""
        common_access_level_group_serialized = CommonAccessLevelGroupSerializer(
            data=request.data
        )
        if not common_access_level_group_serialized.is_valid():
            return validation_error(common_access_level_group_serialized)
        common_access_level_group_serialized.save()

        response_json = {
            "succeeded": True,
            "common_access_level_group": common_access_level_group_serialized.data,
        }

        return Response(response_json, status=200)

    def patch(self, request):
        """edit group"""
        common_access_level_group_obj = CommonAccessLevelGroup.objects.filter(
            id=request.data.get("id")
        ).first()

        common_access_level_group_serialized = CommonAccessLevelGroupSerializer(
            common_access_level_group_obj, data=request.data, partial=True
        )
        if not common_access_level_group_serialized.is_valid():
            return validation_error(common_access_level_group_serialized)
        common_access_level_group_serialized.save()

        response_json = {
            "succeeded": True,
            "common_access_level_group": common_access_level_group_serialized.data,
        }

        return Response(response_json, status=200)

    def delete(self, request):
        """delete group"""
        common_access_level_group_obj = CommonAccessLevelGroup.objects.filter(
            id=request.data.get("id")
        ).first()

        common_access_level_group_obj.delete()

        response_json = {"succeeded": True}

        return Response(response_json, status=200)


class CommonAccessLevelManagementView(APIView):
    """helps to manage common access levels"""

    permission_classes = [CommonAccessLevelManagementPermission]

    def post(self, request):
        """create common access level"""
        common_user_serialized = CommonAccessLevelSerializer(data=request.data)
        if not common_user_serialized.is_valid():
            return validation_error(common_user_serialized)
        common_user_serialized.save()

        response_json = {"succeeded": True,
                         "common_user": common_user_serialized.data}

        return Response(response_json, status=200)

    def patch(self, request):
        """update common access level"""

        common_user_obj = CommonAccessLevel.objects.filter(
            id=request.data.get("id")
        ).first()
        if not common_user_obj:
            return existence_error("common_user")

        common_user_serialized = CommonAccessLevelSerializer(
            common_user_obj, data=request.data, partial=True
        )
        if not common_user_serialized.is_valid():
            return validation_error(common_user_serialized)
        common_user_serialized.save()

        response_json = {
            "succeeded": True,
        }

        return Response(response_json, status=200)

    def delete(self, request):
        """delete common access level"""

        common_user_obj = CommonAccessLevel.objects.filter(
            id=request.data.get("id")
        ).first()

        common_user_obj.delete()

        response_json = {
            "succeeded": True,
        }

        return Response(response_json, status=200)
