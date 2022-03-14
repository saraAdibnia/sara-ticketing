# in this file we have apis that help front-ends to create the access level tree and show it
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from accesslevel.models import AccessLevelSubject, AccessLevelGroup, AccessLevelAction
from accesslevel.serializers import (
    AccessLevelSubjectSerializer,
    AccessLevelGroupSerializer,
    AccessLevelActionSerializer,
)
from accesslevel.permissions import AccessLevelTreePermission
from extra_scripts.EMS import validation_error


class AccessLevelAllSubjectsView(APIView):
    permission_classes = [AccessLevelTreePermission]

    def get(self, request):
        """show all subjects available in the webservice"""

        # query for all subjects
        access_level_subject_objs = AccessLevelSubject.objects.all()

        # serializing data
        access_level_subject_serialized = AccessLevelSubjectSerializer(
            access_level_subject_objs, many=True
        )

        response_json = {
            "succeeded": True,
            "access_level_subjects": access_level_subject_serialized.data,
        }

        return Response(response_json, status=200)


class AccessLevelAllGroupsView(APIView):
    permission_classes = [IsAuthenticated, AccessLevelTreePermission]

    def post(self, request):
        """show all groups availabe in the webservice for a certain subject"""

        # query for all groups in a certain subject
        access_level_group_objs = AccessLevelGroup.objects.filter(
            access_level_subject=request.data.get("access_level_subject")
        )

        # serializing the data
        access_level_group_serialized = AccessLevelGroupSerializer(
            access_level_group_objs, many=True
        )

        response_json = {
            "succeeded": True,
            "access_level_groups": access_level_group_serialized.data,
        }

        return Response(response_json, status=200)


class AccessLevelAllActionsView(APIView):
    permission_classes = [IsAuthenticated, AccessLevelTreePermission]

    def post(self, request):
        """show all actions available in the webservice for a certain group"""

        # query for all actions in a certain group
        access_level_action_objs = AccessLevelAction.objects.filter(
            access_level_group=request.data.get("access_level_group")
        )

        # serializing data
        access_level_action_serialized = AccessLevelActionSerializer(
            access_level_action_objs, many=True
        )

        response_json = {
            "succeeded": True,
            "access_level_actions": access_level_action_serialized.data,
        }

        return Response(response_json, status=200)
