
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from re import sub
from datetime import datetime
from rest_framework.authtoken.models import Token
from utilities import validation_error, existence_error
from extra_scripts.EMS import *
from user.models import User, user

from user.serializers import (
    UserSerializer,
    UserShowSerializer,
    UserEditSerializer,
)
import base64


class ProfileView(APIView):
    """
    This class Views are used to manage User data manipulation and demonstration, so only authenticated user's which have profile in our system should access to this view.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """by calling this method users data are represented in response json for demonstartion intentions"""

        # because of the token in the header django makes a user attribute to request that, users attributes such as id are extractable from it
        # filtering user that the request has been sent from
        user_obj = User.objects.filter(id=request.user.id).first()
        if not user_obj:
            return existence_error("user")

        # serializing queryset
        user_serialized = UserShowSerializer(user_obj)

        response_json = {"succeeded": True, "user": user_serialized.data}
        return Response(response_json, status=200)

    def post(self, request):
        """In this method user can change the user profile fields that wants"""
        user_id = request.user.id
        # finding the user that is making the request
        user_obj = User.objects.filter(id=user_id).first()
        if not user_obj:
            return existence_error("user")

        if request.data.get("email"):
            request.data.update({"email_verified": False})

        # updating user with new data
        user_serialized = UserEditSerializer(
            user_obj, data=request.data, partial=True)
        if not user_serialized.is_valid():
            return validation_error(user_serialized)
        user_serialized.save()

        response_json = {
            "succeeded": True,
        }

        return Response(response_json, status=200)

    def patch(self, request):
        """profile image upload"""
        # finding the user that is making the request
        user_obj = User.objects.filter(id=request.user.id).first()
        if not user_obj:
            return existence_error("user")

        # updating user's profile image
        user_serialized = UserSerializer(
            user_obj,
            data={
                "profile_image": request.data.get("profile_image"),
                # "profile_image_base64" : str(image_64_encode) ,
            },
            partial=True,
        )
        if not user_serialized.is_valid():
            return validation_error(user_serialized)
        user_serialized.save()

        response_json = {
            "succeeded": True,
        }
        return Response(response_json, status=200)

    def delete(self, request):
        """ "delete avatar"""

        # finding the user that is making the request
        user_obj = User.objects.filter(id=request.user.id).first()
        if not user_obj:
            return existence_error("user")

        # deletting photo
        user_serialized = UserSerializer(
            user_obj,
            data={
                "profile_image": None,
                "last_update": datetime.timestamp(datetime.now()),
            },
            partial=True,
        )
        if not user_serialized.is_valid():
            return validation_error(user_serialized)
        user_serialized.save()
        response_json = {
            "succeeded": True,
        }

        return Response(response_json, status=200)


class UserListView(APIView):
    def get(self, request):

        users = User.objects.filter(role=0)
        user_serialized = UserSerializer(users, many=True)
        response_json = {"succeeded": True, "users": user_serialized.data}
        return Response(response_json, status=200)

    def post(self, request):
        user_detail = User.objects.filter(
            id=request.data.get("id")).first()

        user_serialized = UserShowSerializer(user_detail)
        response_json = {"succeeded": True, "user": user_serialized.data}
        return Response(response_json, status=200)


class OperatorUpdatesUser(APIView):
    def get(self, request):
        """by calling this method users data are represented in response json for demonstartion intentions"""

        # because of the token in the header django makes a user attribute to request that, users attributes such as id are extractable from it
        # filtering user that the request has been sent from
        user_obj = User.objects.filter(
            id=request.query_params.get('id')).first()
        if not user_obj:
            return existence_error("user")

        # serializing queryset
        user_serialized = UserShowSerializer(user_obj)

        response_json = {"succeeded": True, "user": user_serialized.data}
        return Response(response_json, status=200)

    def post(self, request):
        """In this method user can change the user profile fields that wants"""
        user_id = request.query_params.get('id')
        # finding the user that is making the request
        user_obj = User.objects.filter(id=user_id).first()
        if not user_obj:
            return existence_error("user")
        if request.data.get("email"):
            request.data.update({"email_verified": False})

        # updating user with new data
        user_serialized = UserEditSerializer(
            user_obj, data=request.data, partial=True)
        if not user_serialized.is_valid():
            return validation_error(user_serialized)
        user_serialized.save()
        # delete the token if user has token
        if request.data.get('is_active') or request.data.get('banned'):
            try:
                tokens = user_obj.auth_token
                if tokens:
                    tokens.delete()
            except:
                pass

        response_json = {
            "succeeded": True,
        }

        return Response(response_json, status=200)

    def patch(self, request):
        """profile image upload"""
        # finding the user that is making the request
        user_obj = User.objects.filter(
            id=request.query_params.get('id')).first()

        if not user_obj:
            return existence_error("user")
        # TODO write object permission instead of this conditions
        # if request.user != user_obj:
        #     if user_obj.role == 1 or request.user.role == 0:
        #         return Response({'description': 'you dont have permission for this action'}, status=403)
        # updating user's profile image
        user_serialized = UserSerializer(
            user_obj,
            data={
                "profile_image": request.data.get("profile_image"),
                # "profile_image_base64" : str(image_64_encode) ,
            },
            partial=True,
        )

        if not user_serialized.is_valid():
            return validation_error(user_serialized)
        user_serialized.save()
        # delete the token if user has token
        if request.data.get('is_active',) or request.data.get('banned'):
            try:
                tokens = user_obj.auth_token
                if tokens:
                    tokens.delete()
            except:
                pass

        response_json = {
            "succeeded": True,
        }
        return Response(response_json, status=200)

    def delete(self, request):
        """ "delete avatar"""

        # finding the user that is making the request
        user_obj = User.objects.filter(
            id=request.query_params.get('id')).first()
        if not user_obj:
            return existence_error("user")
        if request.user != user_obj:
            if user_obj.role == 1 or request.user.role == 0:
                return Response({'description': 'you dont have permission for this action'}, status=403)
        # deletting photo
        user_serialized = UserSerializer(
            user_obj,
            data={
                "profile_image": None,
                "last_update": datetime.timestamp(datetime.now()),
            },
            partial=True,
        )
        if not user_serialized.is_valid():
            return validation_error(user_serialized)
        user_serialized.save()
        response_json = {
            "succeeded": True,
        }

        return Response(response_json, status=200)
