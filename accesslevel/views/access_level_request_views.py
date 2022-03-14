from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from user.models import UserProfile
from user.serializers import UserSerializer
from accesslevel.models import (
    AccessLevelRequest,
    CommonAccessLevel
)
from accesslevel.serializers import (
    AccessLevelRequestSubmitSerializer,
    AccessLevelRequestProceedSerializer,
    AccessLevelRequestShowSerializer,
    CommonAccessLevelSerializer,
    AccessLevelRequestListSerializer
)
from accesslevel.permissions import MyAccessLevelViewSubmitPermission
from extra_scripts.EMS import (
    validation_error,
    existence_error
)
from math import ceil


class MyAccessLevelRequestListView(APIView):
    '''shows the user, access level requests that they have submitted'''
    permission_classes = [MyAccessLevelViewSubmitPermission]

    def post(self, request):
        '''list of my access level requests'''
        allowed_filters = ('negative', 'granted')
        kwargs = {}
        for key, value in request.data.items():
            if key in allowed_filters:
                kwargs.update({key: value})

        n = int(request.data.get('page', 1))
        items_per_page = int(request.data.get('items_per_page', 10))

        try:
            access_level_request_objs = AccessLevelRequest.objects.filter(created_by=request.user.id).filter(
                **kwargs).order_by('-id')[items_per_page*(n-1): items_per_page*(n)]
        except IndexError:
            pass

        access_level_request_serialized = AccessLevelRequestListSerializer(
            access_level_request_objs,
            many=True
        )

        total_filtered = AccessLevelRequest.objects.filter(
            created_by=request.user.id).filter(**kwargs).count()
        pages = ceil(total_filtered/items_per_page)

        response_json = {
            "succeeded": True,
            'pages': pages,
            'total_filtered': total_filtered,
            "access_level_requests": access_level_request_serialized.data
        }

        return Response(response_json, status=200)

    def patch(self, request):
        '''details of a access level request which is mine'''
        access_level_request_obj = AccessLevelRequest.objects.filter(
            id=request.data.get('id'), created_by=request.user.id).first()

        access_level_request_serialized = AccessLevelRequestShowSerializer(
            access_level_request_obj,
        )

        response_json = {
            "succeeded": True,
            "access_level_request": access_level_request_serialized.data
        }

        return Response(response_json, status=200)


class AccessLevelRequestSubmitView(APIView):
    '''helps to submit a access level request'''
    permission_classes = [MyAccessLevelViewSubmitPermission]

    def post(self, request):
        '''create access level request'''

        request.data.update({"created_by": request.user.id})
        access_level_request_serialized = AccessLevelRequestSubmitSerializer(
            data=request.data
        )
        if not access_level_request_serialized.is_valid():
            return validation_error(access_level_request_serialized)
        access_level_request_serialized.save()

        response_json = {
            "succeeded": True,
        }

        return Response(response_json, status=200)

    def delete(self, request):
        '''delete a accesslevel request'''

        access_level_request_obj = AccessLevelRequest.objects.filter(
            id=request.data.get('id'), created_by=request.user.id).first()
        if not access_level_request_obj:
            return existence_error('access_level_request')

        if not access_level_request_obj.created_by.id == request.user.id:
            return Response({"succeeded": False, "details": "this request is not yours to delete"}, status=403)

        if access_level_request_obj.granted is not None:
            return Response({"succeeded": False, "details": "request has been considered and finished. you can not delete it now"}, status=403)

        access_level_request_obj.delete()

        response_json = {
            "succeeded": True
        }
        return Response(response_json, status=200)
