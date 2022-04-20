
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from accesslevel.models import (
    AccessLevelRequest,
    CommonAccessLevel
)
from accesslevel.serializers import (
    AccessLevelRequestListSerializer,
    AccessLevelRequestProceedSerializer,
    AccessLevelRequestSerializer,
    AccessLevelRequestShowSerializer,
    AccessLevelRequestSubmitSerializer,
    CommonAccessLevelSerializer
)
from accesslevel.permissions import AccessLevelManagementPermission
from user.models import User
from user.serializers import UserShowSerializer, UserSerializer

from extra_scripts.EMS import (
    validation_error,
    existence_error
)

from math import ceil


class UserAccessLevelManagementView(APIView):
    '''manage and change a user's access level'''

    permission_classes = [AccessLevelManagementPermission]

    def post(self, request):
        '''change user access level'''
        user_obj = User.objects.filter(
            id=request.data.get('user')).first()
        if not user_obj:
            return existence_error('user')

        # if you want to take access level from user
        if int(request.data.get('negative')):
            user_serialized = UserSerializer(
                user_obj,
                data={
                    "office": "",
                    "common_access_level": "",
                    "role": "0",
                    "access_granted_by": request.user.id,
                },
                partial=True
            )
            if not user_serialized.is_valid():
                return validation_error(user_serialized)
            user_serialized.save()

        # if you want to give access level to user
        else:
            user_serialized = UserSerializer(
                user_obj,
                data={
                    "office": request.data.get('office'),
                    "role": "1",
                    "common_access_level": request.data.get('common_access_level'),
                    "access_granted_by": request.user.id,
                },
                partial=True
            )
            if not user_serialized.is_valid():
                return validation_error(user_serialized)
            user_serialized.save()

        response_json = {
            "succeeded": True
        }

        return Response(response_json, status=200)


class AccessLevelRequestList(APIView):
    '''manage submited access level request by others'''

    permission_classes = [AccessLevelManagementPermission]

    def post(self, request):
        '''list of access level requests'''

        allowed_filters = ('granted', 'negative')
        kwargs = {}
        for key, value in request.data.items():
            if key in allowed_filters:
                kwargs.update({key: value})

        n = int(request.data.get('page', 1))
        items_per_page = int(request.data.get('items_per_page', 10))

        try:
            access_level_request_objs = AccessLevelRequest.objects.filter(
                **kwargs).order_by('-id')[items_per_page*(n-1): items_per_page*(n)]
        except IndexError:
            pass

        access_level_request_serialized = AccessLevelRequestShowSerializer(
            access_level_request_objs,
            many=True,
        )

        total_filtered = AccessLevelRequest.objects.filter(**kwargs).count()
        pages = ceil(total_filtered/items_per_page)

        response_json = {
            "succeeded": True,
            "pages": pages,
            "total_filtered": total_filtered,
            "access_level_requests": access_level_request_serialized.data
        }

        return Response(response_json, status=200)

    def patch(self, request):
        '''details of a access level request'''

        access_level_request_obj = AccessLevelRequest.objects.filter(
            id=request.data.get('id')).first()
        if not access_level_request_obj:
            return existence_error('access_level_request')

        access_level_request_serialized = AccessLevelRequestShowSerializer(
            access_level_request_obj
        )

        response_json = {
            "succeeded": True,
            "access_level_request": access_level_request_serialized.data
        }

        return Response(response_json, status=200)


class AccessLevelRequestProceed(APIView):
    '''helps to handle access level requests. you can reject or accept them by this api'''

    permission_classes = [AccessLevelManagementPermission]

    def post(self, request):

        access_level_request_obj = AccessLevelRequest.objects.filter(
            id=request.data.get('id')).first()
        if not access_level_request_obj:
            return existence_error('access_level_request')

        request.data.update({"granted_by": request.user.id})
        access_level_request_serialized = AccessLevelRequestProceedSerializer(
            access_level_request_obj,
            data=request.data,
            partial=True
        )
        if not access_level_request_serialized.is_valid():
            return validation_error(access_level_request_serialized)
        access_level_request_serialized.save()

        # if the user wants to accept the access level request
        if int(request.data.get('granted')):

            # if access level request is negative(salbi)
            if access_level_request_obj.negative:

                user_obj = User.objects.filter(
                    id=access_level_request_obj.user.id).first()
                user_serialized = UserSerializer(
                    user_obj,
                    data={
                        "office": "",
                        "role": "0",
                        "common_access_level": "",
                        "access_granted_by": request.user.id,
                    },
                    partial=True
                )
                if not user_serialized.is_valid():
                    return validation_error(user_serialized)
                user_serialized.save()

            # if access level request is positive(entesabi)
            else:
                user_obj = User.objects.filter(
                    id=access_level_request_obj.user.id).first()
                user_serialized = UserSerializer(
                    user_obj,
                    data={
                        "office": access_level_request_serialized.data.get('office'),
                        "role": "1",
                        "common_access_level": access_level_request_obj.common_access_level.id,
                        "access_granted_by": request.user.id
                    },
                    partial=True
                )
                if not user_serialized.is_valid():
                    return validation_error(user_serialized)
                user_serialized.save()

            notification_text = 'کاربر گرامی، درخواست سطح دسترسی شما  برای کاربر {} {} مورد بررسی قرار گرفت و قبول شد.'.format(
                access_level_request_obj.user.fname, access_level_request_obj.user.flname)

        # if access is denied and request is rejected
        else:

            notification_text = 'کاربر گرامی، درخواست سطح دسترسی شما برای کاربر {} {} مورد بررسی قرار گرفت و رد شد. با مراجعه به درخواست‌های سطح دسترسی خود جزئیات را مشاهده فرمایید.'.format(
                access_level_request_obj.user.fname, access_level_request_obj.user.flname)

        # creatting notification for the one which submited the request to inform them about outcome of request
        notification_creator(
            user=access_level_request_obj.created_by.id, text=notification_text)

        response_json = {
            "succeeded": True,
        }

        return Response(response_json, status=200)
