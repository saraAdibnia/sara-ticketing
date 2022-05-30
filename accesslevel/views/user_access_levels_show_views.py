# This file contains api's for front-end developers to make the access level for every user in webservice. No other use.


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime as dt
from accesslevel.models import (
    CommonAccessLevel, )
from accesslevel.serializers import (CommonAccessLevelShowSerializer)

from extra_scripts.EMS import (
    validation_error, )

from user.my_authentication.aseman_token_auth import ExpiringTokenAuthentication


class UserAccessLevelShowView(APIView):
    # authentication_classes = [ExpiringTokenAuthentication]

    def get(self, request):
        '''shows all subjects that this user has access to. for frontend use purpose'''
        common_access_level_serialized = CommonAccessLevelShowSerializer(
            request.user.common_access_level )
        # TODO: session last_activity
        # request.session['last_activity'] = dt.now()
        # request.session.modified = True

        response_json = {
            "succeeded": True,
            "access_level": common_access_level_serialized.data
        }

        return Response(response_json, status=200)
