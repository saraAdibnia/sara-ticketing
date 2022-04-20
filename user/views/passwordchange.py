from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView
from utilities import validation_error, existence_error
from extra_scripts.EMS import *
from rest_framework import status
from user.models import User
from user.serializers import UserSerializer


class PasswordChange(APIView):
    """
    This Endpoint has to use cases.
    1) The user just wants to change password without our webservice forcing them to. (handled in post method)
        In this case user should provide old password alongside of new password.
    2) The webservice puts a mandatory term on user to change their password. For now only policy to do so is when user
        has forgotten their password and use sms or email disposable code to login.
        In this case only new password is needed to change pass. 
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """change password not mandatory"""
        # getting old password
        old_pass = request.data.get("old_password")

        # retreiving user object from token in header
        user_obj = User.objects.filter(id=request.user.id).first()
        if not user_obj:
            return existence_error('user')

        # check wether the old password fits or not.
        if user_obj.check_password(old_pass):
            # if old password is provided correctly we update user's password field.
            user_serialized = UserSerializer(
                user_obj,
                data={
                    "password": make_password(request.data.get("password"))
                },
                partial=True
            )
            if not user_serialized.is_valid():
                return validation_error(user_serialized)
            user_serialized.save()

            return Response({"succeeded": True}, status=200)

        # if old password is incorrect.
        else:
            return Response({
                "succeeded": False,
                "details": "Wrong Password. Permission Denied."
            }, status=403)

    def patch(self, request):
        """change password mandatory. (user forgot password)"""

        # retreving user from header token
        user_obj = User.objects.filter(
            id=request.data.get('id')).first()
        if not user_obj:
            return existence_error('user')

        # checking wether it's mandatory for user to change their password or not.
        if user_obj.needs_to_change_pass:
            # changing password
            user_serialized = UserSerializer(user_obj, data={"password": make_password(
                request.data.get("password")), "needs_to_change_pass": False}, partial=True)
            if not user_serialized.is_valid():
                return validation_error(user_serialized)
            user_serialized.save()

            return Response({"succeeded": True}, status=200)
        # if changing password is not forced by our system due to "forgot password" situation, user should not be able to change password by this root
        else:
            return Response({
                "succeeded": False,
                "details": "user can not use this root to change password because changin password for them is not mandatory"
            }, status=403)
