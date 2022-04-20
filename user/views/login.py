import binascii
import os
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from user.my_authentication.aseman_token_auth import MyToken  # TODO doc
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
import uuid
from django.utils import timezone
from utilities import validation_error, existence_error
from user.serializers import UserSerializer
from user.models import User
from user_agents import parse
from datetime import datetime as dt
from django.core.cache import cache
from developinglogs.models import SmsCategory
from extra_scripts.send_sms import send_sms
from history.models import User_log

def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()


def set_wrong_pass_log(user_agent, user_obj, request, kind):
    user_agent = user_agent
    user_agent_spilited = parse(user_agent)
    browser = f"by browser {user_agent_spilited.browser.family} / version {user_agent_spilited.browser.version_string}"
    os = f"by os {user_agent_spilited.os.family} / version {user_agent_spilited.os.version_string}"
    device = f"by device {user_agent_spilited.device.family} /brand {user_agent_spilited.device.brand} model {user_agent_spilited.device.model}"
    for_admin = str(user_agent_spilited)
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    user_log = User_log.objects.create(
        log_kind=kind,  # Wrong Password
        browser=browser,
        os=os,
        device=device,
        ip_address=ip,
        for_admin=for_admin,
        user=user_obj,
    )

    user_log.save()


class UserLoginApiView(APIView):
    """
        login for normal user 
    """
    def post(self, request):
        # if information given is not enough to go through any method of logging in.

        if request.data.get("username") and request.data.get("password"):

            # filtering user
            user_obj = User.objects.filter(
                mobile=request.data.get("username")
            ).first()
            # checking that user exists matching credentials provided
            if not user_obj:
                return existence_error("User")

            if user_obj.banned:
                response_json = {"succeeded": False,
                                 "details": "you are banned"}
                return Response(response_json, status=403)

            if not user_obj.is_active:
                response_json = {
                    "succeeded": False,
                    "details": "this user has not verified mobile phone. try to do so",
                }
                return Response(response_json, status=406)

            if user_obj.role != 0:
                response_json = {
                    "succeeded": False,
                    "details": "This Method of obtaining token is only for simple users",
                }
                return Response(response_json, status=400)
            # checking password
            if user_obj.check_password(request.data.get("password")):

                # getting or creating token
                
                MyToken.objects.filter(
                    user=user_obj).delete()

                token = MyToken.objects.create(user=user_obj)

                user_obj.temp_password= None
                user_obj.last_login  = timezone.now()
                user_obj.save()


                # successful login
                response_json = {
                    "succeeded": True,
                    "Authorization": "Token {}".format(token.key),
                    "role": user_obj.role,
                }
                # set user_log for successful login
                set_wrong_pass_log(request.headers.get(
                    "User-Agent"), user_obj, request, kind=0)

                return Response(response_json, status=200)

            # if the provided password by user is wrong.
            else:
                response_json = {
                    "succeeded": False,
                    "details": "Wrong Password. Permission Denied.",
                }

                set_wrong_pass_log(request.headers.get(
                    "User-Agent"), user_obj, request, kind=1)
                return Response(response_json, status=403)
        else:
            return Response(
                {
                    "succeeded": False,
                    "details": "Authentication credentials were not provided.",
                },
                status=401,
            )


class CorporateLogin(APIView):
    def post(self, request):
        """corporate login send sms"""
    # we generate a for digit int random number
        code = str(uuid.uuid4().int)[:5]

    # filtering user
        user_obj = User.objects.filter(
            mobile=request.data.get("username")
        ).first()
        if not user_obj:
            return existence_error("User")
        if user_obj.banned:
            return Response({"succeeded": False, "details": "you are banned"})
        if user_obj.role == 0:
            return Response(
                {
                    "succeeded": False,
                    "details": "This Method of loging-in is just for corporate users",
                },
                status=400,
            )

        if user_obj.check_password(request.data.get("password")):
        # set token for users with direct_login

            if user_obj.direct_login:
                

                MyToken.objects.filter(
                    user=user_obj).delete()

                token = MyToken.objects.create(user=user_obj)

                # user should change their password if they login successfuly via this method. so:
                user_obj.temp_password= None
                user_obj.last_login  = timezone.now()
                user_obj.save()

                response_json = {
                    "succeeded": True,
                    "Authorization": "Token {}".format(token.key),
                    "role": user_obj.role,
                }
                
                return Response(response_json, status=200)
            key = f'login_sms_try-{user_obj.mobile}'
            if cache.get(key): # pass the sms code sending if we already have send an sms to user
                print('****************************'*4)
                return Response({'remain_time': f'{cache.ttl(key)}'}, status= 200)


            user_serialized = UserSerializer(
                user_obj, data={"temp_password": make_password(code)}, partial=True
            )

            if not user_serialized.is_valid():
                return validation_error(user_serialized)
            user_serialized.save()
            smsCategory_obj = SmsCategory.objects.filter(code=1).first()
            if smsCategory_obj.isActive == True:
                sms_text = smsCategory_obj.smsText.format(code)
                send_sms(
                    user_obj.mobile,
                    sms_text,
                    smsCategory_obj.id,
                    smsCategory_obj.get_sendByNumber_display(),
                    request.user.id,
                )
            response_json = {"succeeded": True, "code": code}

            # set the try_again for sending sms login to prevent from sending alot of sms
            cache.set(f'login_sms_try-{user_obj.mobile}','value', 120) 

            return Response(response_json, status=200)


        # if the password was wrong
        else:
            set_wrong_pass_log(request.headers.get(
                "User-Agent"), user_obj, request, kind=1)

            response_json = {
                "succeeded": False,
                "details": "Wrong Password. Permission Denied.",
            }
            return Response(response_json, status=403)

    def patch(self, request):
        """corporate login second factor call back"""

        user_obj = User.objects.filter(
            mobile=request.data.get("mobile")).first()
        # checking that user exists matching credentials provided
        if not user_obj:
            return existence_error("User")

        if user_obj.banned:
            response_json = {"succeeded": False, "details": "you are banned"}
            return Response(response_json, status=403)

        if not user_obj.is_active:
            response_json = {
                "succeeded": False,
                "details": "this user has not verified mobile phone. try to do so",
            }
            return Response(response_json, status=406)

        # checking temp password that has been created while sending sms. if the user exists the token will generate or taken from database
        if user_obj.check_temppassword(request.data.get("password")):

            MyToken.objects.filter(
                user=user_obj).delete()
            token = MyToken.objects.create(user=user_obj)

            # user should change their password if they login successfuly via this method. so:
            
            user_obj.temp_password= None
            user_obj.last_login  = timezone.now()
            user_obj.save()
            # successful login
            response_json = {
                "succeeded": True,
                "Authorization": "Token {}".format(token.key),
                "role": user_obj.role,
            }

            set_wrong_pass_log(request.headers.get(
                "User-Agent"), user_obj, request, kind=0)
            # TODO check with front later

            return Response(response_json, status=200)

        # if the password is wrong
        else:

            set_wrong_pass_log(request.headers.get(
                "User-Agent"), user_obj, request, kind=3)

            response_json = {
                "succeeded": False,
                "details": "Wrong Password. Permission Denied...",
            }
            return Response(response_json, status=403)


class ChangeToken(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_obj = request.user
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            # there may be an 401 error when user does not provide authorization in header or the data is wrong.
            pass

        token, created = MyToken.objects.get_or_create(user=user_obj)

        response_json = {
            "succeeded": True,
            "Authorization": "Token {}".format(token.key),
        }
        return Response(response_json, status=200)
