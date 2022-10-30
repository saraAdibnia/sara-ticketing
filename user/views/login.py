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
from icecream import ic
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from django.views.decorators.cache import cache_page

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
    def post(self , request):
    
        """corporate login send sms"""
    # we generate a for digit int random number
        code = str(uuid.uuid4().int)[:5]

    # filtering user
        user_obj = User.objects.filter(
        Q(mobile=request.data.get("username")) |
        Q(email=request.data.get("username")) 
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
                return Response({'remain_time': f'{cache.ttl(key)}' , "succeeded": 'True' }, status= 200)


            user_serialized = UserSerializer(
                user_obj, data={"temp_password": make_password(code)}, partial=True
            )

            if not user_serialized.is_valid():
                return validation_error(user_serialized)
            user_serialized.save()
            if request.data.get("email"):
                subject, from_email, to = 'hello', 'asemanpost@gmail.com', normalize_email(request.data.get("email"))
                # url_address = 'http://localhost:8000/user/verify_email_back/{}'.format(code)
                text_content = 'Verify Your Email'
                html_content = '<html><head><meta charset="utf-8" /><meta http-equiv="x-ua-compatible" content="ie=edge" /><title>Email Confirmation</title><meta name="viewport" content="width=device-width, initial-scale=1" /><style type="text/css">  @media screen { @font-face {font-family: "Source Sans Pro";font-style: normal;font-weight: 400;src: local("Source Sans Pro Regular"), local("SourceSansPro-Regular"),url(https://fonts.gstatic.com/s/sourcesanspro/v10/ODelI1aHBYDBqgeIAH2zlBM0YzuT7MdOe03otPbuUS0.woff) format("woff");}@font-face {font-family: "Source Sans Pro";font-style: normal;font-weight: 700;src: local("Source Sans Pro Bold"), local("SourceSansPro-Bold"),url(https://fonts.gstatic.com/s/sourcesanspro/v10/toadOcfmlt9b38dHJxOBGFkQc6VGVFSmCnC_l7QZG60.woff) format("woff");}}body,table,td,a {-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;}table,td {mso-table-rspace: 0pt;mso-table-lspace:0pt;}img {-ms-interpolation-mode: bicubic;}a[x-apple-data-detectors] {font-family: inherit !important; font-size: inherit !important;font-weight: inherit !important;line-height: inherit !important; color: inherit !important; text-decoration: none !important;}div[style*="margin: 16px 0;"] { margin: 0 !important;  }  body { width: 100% !important;height: 100% !important; padding: 0 !important; margin: 0 !important;  }  table { border-collapse: collapse !important;  }  button {background-color: #1a82e2;color: #ffffff;border: none;outline: none;display: inline-block;padding: 16px 36px;font-family: "Source Sans Pro", Helvetica, Arial, sans-serif;font-size: 16px;border-radius: 6px;font-size: 2.5rem;  }  img {height: auto line-height: 100%;text-decoration: none;border: 0; outline: none;  }</style></head><body style="background-color: #e9ecef"><div  class="preheader"  style="display: none; max-width: 0; max-height: 0; overflow: hidden; font-size: 1px; line-height: 1px; color: #fff; opacity: 0">  A preheader is the short summary text that follows the subject line when an email is viewed in the inbox.</div><table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-top: 6rem">  <tr> <td align="center" bgcolor="#e9ecef"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px"> <tr><td align="left" bgcolor="#ffffff" style="padding: 36px 24px 0; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif"> <h1 style="margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -1px; line-height: 48px">Confirm Your Email Address</h1></td> </tr></table> </td>  </tr>  <tr> <td align="center" bgcolor="#e9ecef"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px"> <tr><td align="left" bgcolor="#ffffff" style="padding: 24px; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px"> <p style="margin: 0">It seems that you want to verify your email in our website. Please copy the code below to do so :</p></td> </tr> <tr><td align="left" bgcolor="#ffffff"> <table border="0" cellpadding="0" cellspacing="0" width="100%"><tr> <td align="center" bgcolor="#ffffff" style="padding: 12px"><table border="0" cellpadding="0" cellspacing="0"> <tr><td align="center" bgcolor="#1a82e2" style="border-radius: 6px"> <button>' + format(code) + '</button></td></tr></table></td></tr></table></td></tr><tr><td align="left" bgcolor="#ffffff" style="padding: 24px; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px" ><p style="margin: 0">Aseman Sooye Parsian, 14th valley, Pakestan st, Beheshti st.</p><p style="margin: 0">Email Address : info@asemanexpress.com</p><p style="margin: 0">Phone number: +9821-45312</p></td></tr></table></td></tr><tr><td align="center" bgcolor="#e9ecef" style="padding: 24px"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px"><tr><td align="center" bgcolor="#e9ecef" style=" padding: 12px 24px; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif; font-size: 14px; line-height: 20px; color: #666; " ><p style="margin: 0"> You received this email because we received a request for valifation for your account. If you didn t request validation you can safely delete this email.</p></td></tr><tr><td align="center" bgcolor="#e9ecef" style=" padding: 12px 24px; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif; font-size: 14px; line-height: 20px; color: #666; " ></td></tr></table></td></tr></table></body></html>'
               
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                # msg.body(format(code))
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return Response({"succeeded": True, "code": code}, status=200)
            if request.data.get("mobile"):
                smsCategory_obj = SmsCategory.objects.filter(code=1).first()
                if smsCategory_obj:
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
                cache.set(f'login_sms_try-{user_obj.mobile}' ,'value' ,120)

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
