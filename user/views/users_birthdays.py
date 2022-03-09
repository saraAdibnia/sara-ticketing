from rest_framework.views import APIView
from user.models import UserProfile
from rest_framework.response import Response
from utilities import existence_error, validation_error
from user.my_authentication.aseman_token_auth import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from user.serializers import  UserBirthdaysSerialzier
from math import ceil
# from developinglogs.serializers.sms_log_serializers import SmsCategorySerializer
# from developinglogs.models.sms_log_models import SmsCategory
from history.models import User_log
import binascii
import os
from user.my_authentication.aseman_token_auth import MyToken  # TODO doc
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework.settings import api_settings
from rest_framework import status
from django.db.models import Q
import uuid
from django.utils import timezone
from extra_scripts.emailnormalization import normalize_email
from user.serializers import UserSerializer
# from extra_scripts.send_sms import send_sms
from user_agents import parse
from datetime import datetime as dt
from django.core.cache import cache


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


class UsersBirthdays(APIView):  # TODO set permissions
    permission_classes = [IsAuthenticated]
    # get the reuqest user files

    def get(self, request):
        '''list of my access level requests'''

        n = int(request.query_params.get('page', 1))
        items_per_page = int(request.query_params.get('items_per_page', 10))

        month = request.GET.get('month')
        main_query = UserProfile.objects.filter(
            birthday__month=month)
        serializers = UserBirthdaysSerialzier(main_query, many=True)

        type0 = main_query.filter(role=0)
        type1 = main_query.filter(role=1)
        type2 = main_query.filter(role=2)

        serializers0 = UserBirthdaysSerialzier(type0, many=True)
        serializers1 = UserBirthdaysSerialzier(type1, many=True)
        serializers2 = UserBirthdaysSerialzier(type2, many=True)

        return Response({'total_users': len(main_query),
                        #  'pages': ceil(len(main_query) / items_per_page),
                         'type_zero': serializers0.data,
                         'total_zero': len(type0),
                         'type_one': serializers1.data,
                         'total_one': len(type1),
                         'type_two': serializers2.data,
                         'total_two': len(type2),
                         }, status=200)


class UserBirthdayByLink(APIView):
    def post(self, request):
        user_obj = UserProfile.objects.filter(
            mobile=request.data.get('mobile')).last()
        if user_obj is None:
            return existence_error('user')
        code = str(uuid.uuid4().int)[:5]
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
        response_json = {"succeeded": True}
        return Response(response_json, status=200)

    def patch(self, request):
        user_obj = UserProfile.objects.filter(
            mobile=request.data.get("mobile")).first()
        # checking that user exists matching credentials provided
        if not user_obj:
            return existence_error("User")

        if user_obj.banned:
            response_json = {"succeeded": False, "details": "you are banned"}
            return Response(response_json, status=403)

        # checking temp password that has been created while sending sms. if the user exists the token will generate or taken from database
        if user_obj.check_temppassword(request.data.get("password")):

            old_token = Token.objects.filter(
                user=user_obj).all()
            for token in old_token:
                token.delete()

            old_token2 = MyToken.objects.filter(
                user=user_obj).all()

            for token in old_token2:
                token.delete()

            token = MyToken.objects.create(user=user_obj)
            token.save()
            print('yeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeees \n\n\n ')

            # user should change their password if they login successfuly via this method. so:
            user_serialized = UserSerializer(
                user_obj,
                data={"temp_password": None, "last_login": timezone.now(), },
                partial=True,
            )

            if not user_serialized.is_valid():
                return validation_error(user_serialized)
            user_serialized.save()

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

    def put(self, request):
        if request.user.is_authenticated:
            serializers = UserSerializer(
                request.user,
                data={'birthday': request.data.get('birthday'),
                      'gender': request.data.get('gender')}, partial=True)
            if serializers.is_valid():
                instance = serializers.save()
            else:
                return validation_error(serializers)
            jr = {'succeed': True, 'user_data': UserSerializer(instance).data}
            return Response(jr, status=200)
        else:
            return Response({'succeed': False, 'error': 'AuthenticationFailed'}, status=401)
