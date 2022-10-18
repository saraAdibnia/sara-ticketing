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
                "dial_code" : request.data.get("dial_code"),
                # passwords should never be saved without turning into hash. it's unethical and this system won't work.
                "temp_password": make_password(code),
                "is_active": False,  # user activates when they verify their phone number
                "is_real": request.data.get("is_real"),
            }
            if request.data.get("email"):
                req.update({"email": request.data.get("email")})
                user_serialized = UserSerializer(data=req)
                subject, from_email, to = 'hello', 'sara.adibi2000@gmail.com', normalize_email(request.data.get("email"))
                url_address = 'http://localhost:8000/user/verify_email/'
                text_content = 'Verify Your Email'
                html_content = '<html> <head> <meta http-equiv="Content-Type" content="text/html; charset=uf8" /> </head> <body style="text-align: center ;"> <img src="https://asemanexpress.com/wp-content/uploads/2020/06/h-logo.png" style="width: 248px; height: 106px" /> <h1>Email Verification</h1> <p>It seems that you want to verify your email in our website. Please click on the link below to do so:<p> <p>به نظر می‌رسد شما می‌خواهید ایمیل خود را در سامانه ما تایید کنید. برای انجام اینکار بر روی لینک زیر کلیک کنید: </p> <form action={}> <input style="background:none; border:none; color:#fff; margin-top:1rem; width:300px ; padding: 2rem ;background: #383030 ; color: aliceblue ; display: block ; margin: auto; border-radius: 20px ; text-align: center" type="submit" value="اعتبارسنجی ایمیل" /> </form> <p>If you did not request this you can safely ignore this email.<p> <p> .اگر شما درخواست نداده‌اید، به سادگی از این ایمیل صرف نظر کنید. </p> <p>We love hearing from you.</p> <p> Aseman Sooye Parsian, Vahabi Barzi valley, 16th st., Ghanbarzade, Beheshti st., Tehran, Iran. </p> <p>Phone number: +9821-45312</p> <p>Email Address: info@asemanexpress.com</p> </body> </html>'.format(url_address)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            # this condition meets when the user is new if the mobile phone length has been checked on frontend to not to exeed 100 characters.

            if user_serialized.is_valid():
                user_serialized.save()
                
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
        user.save()
        return Response({'succeeded':True}, status=200)