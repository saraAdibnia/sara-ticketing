
from django.db import reset_queries
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from re import sub
from datetime import datetime
from rest_framework.authtoken.models import Token
from user.my_authentication.aseman_token_auth import MyToken
from utilities import validation_error, existence_error
from extra_scripts.EMS import *
from django.utils import timezone
from user.models import User, user
from io import StringIO
from PIL import Image
from user.serializers import (
    UserSerializer,
    UserShowSerializer,
    UserEditSerializer,
)
from django.contrib.auth.hashers import make_password
from developinglogs.models.sms_log_models import SmsCategory
from extra_scripts.send_sms import send_sms
import base64
from icecream import ic
import uuid


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

        # finding the user that is making the request
        user_obj = request.user
        if request.data.get("email"):
            request.data.update({"email_verified": False})
        # TODO: refactor this part of the code to not repeat the code in if and out of it

            # TODO: uncomment this when u want to send actual sms
            # smsCategory_obj = SmsCategory.objects.filter(code=1).first()
            # sms_text = smsCategory_obj.smsText.format(code)
            # send_sms(
            #     user_serialized.data.get("mobile"),
            #     sms_text,
            #     smsCategory_obj.id,
            #     smsCategory_obj.get_sendByNumber_display(),
            #     request.user.id,
            #     )

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
        user_obj = request.user
        ic(type(request.data.get('profile_image')))
        ic(user_obj.id)
        # updating user's profile image
        user_serialized = UserSerializer(
            user_obj,
            data={
                "profile_image": request.data['profile_image'],
            },
            partial=True,
        )

        # image_file = StringIO.StringIO(user_obj.profile_image.read())
        if not user_serialized.is_valid():
            return validation_error(user_serialized)
        user_serialized.save()

        # user_serialized.profile_image =  user_serialized.get_image()
        # ic(User.get_image())

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


class UpdatePhoneNumber(APIView):

    def post(self, request):
        user_id = request.data.get("user")
        user_obj =User.objects.filter(id = user_id).first()
        code = str(uuid.uuid4().int)[:5]
        user_obj.temp_password = make_password(code)
        user_obj.save()
        ic(user_obj.temp_password )
        request.data.get("mobile")
        return Response({"succeeded": True, "code": code}, status=200)

    def patch(self, request):
        # mobile number and temprorilly password that has been sent to user via sms in signup view is given by user
        user_id = request.data.get("user")
        mobile = request.data.get("mobile")
        temp_password =request.data.get("temp_password")

        # we filter and find the user
        user_obj = User.objects.filter(id=user_id).first()
        ic(user_obj)
        if not user_obj:
            return existence_error("user")

        # check if the temp pass provided by user is the one that has been sent via sms
        ic(temp_password)
        if user_obj.check_temppassword(temp_password):
            # activating the user if password is correct
            old_token = Token.objects.filter(user=user_obj).last()
            if old_token:
                old_token.delete()
            # ic(user_obj)
            old_token = MyToken.objects.filter(
                user=user_obj).last()
            if old_token:
                old_token.delete()

            token = MyToken.objects.create(user=user_obj)
            token.save()

            user_serialized = UserSerializer(
                user_obj,
                data={
                    "is_active": True,
                    "temp_password": None,
                    "last_login": timezone.now(),
                    "mobile": mobile, }, partial=True,
            )
            if not user_serialized.is_valid():
                return validation_error(user_serialized)
            user_serialized.save()
            # TODO : check if the django history works
            response_json = {
                "succeeded": True,
                "Authorization": "Token {}".format(token.key),
                "role": user_obj.role,
                # "record":  User.history.first(),
            }
            return Response(response_json, status=200)
        # this condition meets if the temp password provided by user is wrong
        else:
            response_json = {
                "succeeded": False,
                "details": "Wrong Password. Permission Denied.",
            }

        return Response(response_json, status=403)


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
        code = str(uuid.uuid4().int)[:5]
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
