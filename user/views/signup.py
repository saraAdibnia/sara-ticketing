from click import confirmation_option
from django.http.response import JsonResponse
from developinglogs.models.sms_log_models import SmsCategory
from extra_scripts.emailnormalization import normalize_email
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
import uuid
from django.core.mail import EmailMultiAlternatives
from user.serializers import UserSerializer, EVFPSerializer
from user.models import User
from extra_scripts.EMS import *
from extra_scripts.kavenegar import *
from extra_scripts.send_sms import send_sms 
from rest_framework.authtoken.models import Token
from user.my_authentication.aseman_token_auth import MyToken
from django.utils import timezone
from user.models import Captcha
from captcha.image import ImageCaptcha
import os
from System.permissions import EditTickets, IsOperator
from rest_framework.permissions import IsAuthenticated
from icecream import ic
from utilities import validation_error, existence_error
from utilities.pagination import CustomPagination
from rest_framework import generics



# from verify_email.email_handler import send_verification_email
class SignupView(APIView):
    """
    if a user want's to signup in this web service there are two mandatory fields (password, mobile phone number) and one optional(email)
    *user must verify the mobile phone is theirs. this would be specified by offering 4 digit int code that has been sent to them
    """

    def post(self, request):
        """
        user should provide username, password, mobile num and email(optional). this view does the logic of signing up afterwards.
        after that the verify code is sent by this view, front-end should take the mentioned code and send it to verifyphonenumber view in this file.
        as long as the user has not provided the code to that view, his account would be inactive (handled by is_active field in user model)
        NOTE: in this view if the front-end get succeeded parmater as true, he should ask for the code and send the code to mobile verification view
        """

        # before start the user registraton process we check the captcha and its code validation which was created to user in /use/captcha/ > get /
        captcha_obj = Captcha.objects.filter(id=request.data.get('captcha_id')).first()
        if not captcha_obj:
            return existence_error('captcha')
        
        if request.data.get('code').upper()!=captcha_obj.code:
            response_json = {
                'succeeded': False
            }
            os.remove('.'+captcha_obj.captcha)
            captcha_obj.delete()
            return Response(response_json, status=402)
            
        code = str(uuid.uuid4().int)[:5]
        # # first we check that the user does not exist actively
       
        user_obj = User.objects.filter(mobile=request.data.get("mobile")).first()
        if not user_obj:
            print('user is here \n\n\n\n\n\n\n\n')
            # we generate a for digit int random number
            req = {
                # passwords should never be saved without turning into hash. it's unethical.
                "password": make_password(request.data.get("password")),
                "mobile": request.data.get("mobile"),
                "fname" : request.data.get("fname"),
                "flname" : request.data.get("flname"),
                "email" : request.data.get("email"),
                "dial_code" : request.data.get("dial_code"),
                # passwords should never be saved without turning into hash. it's unethical and this system won't work.
                "temp_password": make_password(code),
                "is_active": False,  # user activates when they verify their phone number
                "is_real": request.data.get("is_real"),
            }
            user_serialized = UserSerializer(data=req)
            if user_serialized.is_valid():
                user_serialized.save()
    
            else:
                return validation_error(user_serialized)

                
            if request.data.get('with_email'):
                req.update({"with_email": request.data.get("with_email")})
                subject, from_email, to = 'hello', 'asemanpost@gmail.com', normalize_email(request.data.get("email"))
                # url_address = 'http://localhost:8000/user/verify_email_back/{}'.format(code)
                text_content = 'Verify Your Email'
                html_content = '<html><head><meta charset="utf-8" /><meta http-equiv="x-ua-compatible" content="ie=edge" /><title>Email Confirmation</title><meta name="viewport" content="width=device-width, initial-scale=1" /><style type="text/css">  @media screen { @font-face {font-family: "Source Sans Pro";font-style: normal;font-weight: 400;src: local("Source Sans Pro Regular"), local("SourceSansPro-Regular"),url(https://fonts.gstatic.com/s/sourcesanspro/v10/ODelI1aHBYDBqgeIAH2zlBM0YzuT7MdOe03otPbuUS0.woff) format("woff");}@font-face {font-family: "Source Sans Pro";font-style: normal;font-weight: 700;src: local("Source Sans Pro Bold"), local("SourceSansPro-Bold"),url(https://fonts.gstatic.com/s/sourcesanspro/v10/toadOcfmlt9b38dHJxOBGFkQc6VGVFSmCnC_l7QZG60.woff) format("woff");}}body,table,td,a {-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;}table,td {mso-table-rspace: 0pt;mso-table-lspace:0pt;}img {-ms-interpolation-mode: bicubic;}a[x-apple-data-detectors] {font-family: inherit !important; font-size: inherit !important;font-weight: inherit !important;line-height: inherit !important; color: inherit !important; text-decoration: none !important;}div[style*="margin: 16px 0;"] { margin: 0 !important;  }  body { width: 100% !important;height: 100% !important; padding: 0 !important; margin: 0 !important;  }  table { border-collapse: collapse !important;  }  button {background-color: #1a82e2;color: #ffffff;border: none;outline: none;display: inline-block;padding: 16px 36px;font-family: "Source Sans Pro", Helvetica, Arial, sans-serif;font-size: 16px;border-radius: 6px;font-size: 2.5rem;  }  img {height: auto line-height: 100%;text-decoration: none;border: 0; outline: none;  }</style></head><body style="background-color: #e9ecef"><div  class="preheader"  style="display: none; max-width: 0; max-height: 0; overflow: hidden; font-size: 1px; line-height: 1px; color: #fff; opacity: 0">  A preheader is the short summary text that follows the subject line when an email is viewed in the inbox.</div><table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-top: 6rem">  <tr> <td align="center" bgcolor="#e9ecef"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px"> <tr><td align="left" bgcolor="#ffffff" style="padding: 36px 24px 0; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif"> <h1 style="margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -1px; line-height: 48px">Confirm Your Email Address</h1></td> </tr></table> </td>  </tr>  <tr> <td align="center" bgcolor="#e9ecef"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px"> <tr><td align="left" bgcolor="#ffffff" style="padding: 24px; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px"> <p style="margin: 0">It seems that you want to verify your email in our website. Please copy the code below to do so :</p></td> </tr> <tr><td align="left" bgcolor="#ffffff"> <table border="0" cellpadding="0" cellspacing="0" width="100%"><tr> <td align="center" bgcolor="#ffffff" style="padding: 12px"><table border="0" cellpadding="0" cellspacing="0"> <tr><td align="center" bgcolor="#1a82e2" style="border-radius: 6px"> <button>' + format(code) + '</button></td></tr></table></td></tr></table></td></tr><tr><td align="left" bgcolor="#ffffff" style="padding: 24px; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px" ><p style="margin: 0">Aseman Sooye Parsian, 14th valley, Pakestan st, Beheshti st.</p><p style="margin: 0">Email Address : info@asemanexpress.com</p><p style="margin: 0">Phone number: +9821-45312</p></td></tr></table></td></tr><tr><td align="center" bgcolor="#e9ecef" style="padding: 24px"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px"><tr><td align="center" bgcolor="#e9ecef" style=" padding: 12px 24px; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif; font-size: 14px; line-height: 20px; color: #666; " ><p style="margin: 0"> You received this email because we received a request for valifation for your account. If you didn t request validation you can safely delete this email.</p></td></tr><tr><td align="center" bgcolor="#e9ecef" style=" padding: 12px 24px; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif; font-size: 14px; line-height: 20px; color: #666; " ></td></tr></table></td></tr></table></body></html>'
               
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                # msg.body(format(code))
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return Response({"succeeded": True, "code": code}, status=200)
            

            else:
                smsCategory_obj = SmsCategory.objects.filter(code=1).first()
                ic(smsCategory_obj)
                if smsCategory_obj.isActive == True:
                    sms_text = smsCategory_obj.smsText.format(code)
                    send_sms(
                        user_serialized.data.get("mobile"),
                        sms_text,
                        smsCategory_obj.id,
                        smsCategory_obj.get_sendByNumber_display(),
                        request.user.id,
                    )

                    return Response({"succeeded": True, "code": code}, status=200)
            # this condition meets when the user is new if the mobile phone length has been checked on frontend to not to exeed 100 characters.
           
            if user_serialized.is_valid():
                user_serialized.save()
    
            else:
                return validation_error(user_serialized)
        # this condition meets when user is not new
        elif not user_obj.is_active:
            print('user is not ative \n\n\n\n\n\n\n\n')

            req = {
                "temp_password": make_password(code),
                "password": make_password(request.data.get("password")),
                "is_real": request.data.get("is_real"),
            }
            if request.data.get("email"):
                request.data.update({"email": request.data.get("email")})
              

            # new temperory password is generated for user and sent to them via sms. user should be redirected to mobile number verification
            user_serialized = UserSerializer(user_obj, data=req, partial=True)
            if not user_serialized.is_valid():
                return validation_error(user_serialized)
            user_serialized.save()
            smsCategory_obj = SmsCategory.objects.filter(code=1).first()
            sms_text = smsCategory_obj.smsText.format(code)
            if smsCategory_obj.isActive == True:

                send_sms(
                    user_obj.mobile,
                    sms_text,
                    smsCategory_obj.id,
                    smsCategory_obj.get_sendByNumber_display(),
                    request.user.id,
                )

            return Response({"succeeded": True, "code": code}, status=200)
        else:
            print('user is already active \n\n\n\n\n\n\n\n')

            response_json = {
                "succeeded": False,
                "details": "user exists, please try to login",
            }

            return Response(response_json, status=406)


class VerifyPhoneNumber(APIView):
    """
    this view would be called when the user has sent data to sign-up view and wants to verify their mobile number and activate their account
    """

    def post(self, request):
        # mobile number and temprorilly password that has been sent to user via sms in signup view is given by user
        mobile = request.data.get("mobile")
        temp_password = request.data.get("temp_password")

        # we filter and find the user
        user_obj = User.objects.filter(mobile=mobile).first()
        if not user_obj:
            return existence_error("user")

        # check if the temp pass provided by user is the one that has been sent via sms
        if user_obj.check_temppassword(temp_password):
            # activating the user if password is correct
            old_token = Token.objects.filter(user=user_obj).last()
            if old_token:
                old_token.delete()

            old_token = MyToken.objects.filter(
                user=user_obj).last()
            if old_token:
                old_token.delete()

            token = MyToken.objects.create(user=user_obj)
            token.save()

            
            user_serialized = UserSerializer(
                user_obj, data={"temp_password": None, "last_login": timezone.now() , "confirmation" : 1}, partial=True,
            )
            if not user_serialized.is_valid():
                return validation_error(user_serialized)
            user_serialized.save()

            response_json = {
                "succeeded": True,
                "Authorization": "Token {}".format(token.key),
                "role": user_obj.role,
            }
            return Response(response_json, status= 200)
        # this condition meets if the temp password provided by user is wrong
        else:
            response_json = {
                "succeeded": False,
                "details": "Wrong Password. Permission Denied.",
            }

        return Response(response_json, status=403)
    
class Confirm(generics.UpdateAPIView):
    permission_classes = [IsOperator , IsAuthenticated]
    def get_object(self):
        return User.objects.filter(confirmation = 1).first()
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.confirmation = 2
        user.role = 1
        user.is_active = True
        user.direct_login = True
        user.save()
        return Response({'succeeded':True}, status=200)