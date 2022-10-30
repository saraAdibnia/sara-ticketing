from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import uuid
from user.serializers import UserSerializer, EVFPSerializer
from user.models import User, EVFP
# from extra_scripts.EMS import *
from utilities import existence_error, validation_error
from rest_framework.authtoken.models import Token
from user.my_authentication.aseman_token_auth import MyToken
from django.utils import timezone
class VerifyEmailView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        '''By calling this view if user has a registered email in their account a four digit code would be emailed to them in order to verify it'''

        user_obj = User.objects.filter(id=request.user.id).first()
        if not user_obj:
            return existence_error('user')

        if user_obj.email:
            # generating a random code
            code = str(uuid.uuid4())

            EVFP_serialized = EVFPSerializer(
                data={
                    "user": request.user.id,
                    "code": code
                }
            )
            if not EVFP_serialized.is_valid():
                return validation_error(EVFP_serialized)
            EVFP_serialized.save()

            # url_address = 'http://localhost:8000/user/verify_email/{}'.format(code)
            # # sending new temp password to user
            # subject, from_email, to = 'hello', 'test@asemanexpress.com', normalize_email(
            #     request.user.email)
            # text_content = 'Verify Your Email'

            # sr = '<html> <head> <meta http-equiv="Content-Type" content="text/html; charset=uf8" /> </head> <body style="text-align: center ;"> <img src="https://asemanexpress.com/wp-content/uploads/2020/06/h-logo.png" style="width: 248px; height: 106px" /> <h1>Email Verification</h1> <p>It seems that you want to verify your email in our website. Please click on the link below to do so:<p> <p>به نظر می‌رسد شما می‌خواهید ایمیل خود را در سامانه ما تایید کنید. برای انجام اینکار بر روی لینک زیر کلیک کنید: </p> <form action={}> <input style="background:none; border:none; color:#fff; margin-top:1rem; width:300px ; padding: 2rem ;background: #383030 ; color: aliceblue ; display: block ; margin: auto; border-radius: 20px ; text-align: center" type="submit" value="اعتبارسنجی ایمیل" /> </form> <p>If you did not request this you can safely ignore this email.<p> <p> .اگر شما درخواست نداده‌اید، به سادگی از این ایمیل صرف نظر کنید. </p> <p>We love hearing from you.</p> <p> Aseman Sooye Parsian, Vahabi Barzi valley, 16th st., Ghanbarzade, Beheshti st., Tehran, Iran. </p> <p>Phone number: +9821-45312</p> <p>Email Address: info@asemanexpress.com</p> </body> </html>'.format(
            #     url_address)

            # msg = EmailMultiAlternatives(
            #     subject, text_content, from_email, [to])
            # msg.attach_alternative(sr, "text/html")
            # msg.send()

            response_json = {
                'succeeded': True
            }
        else:
            response_json = {
                'succeeded': False
            }
        return Response(response_json, status=200)


class VerifyEmailCallBack(APIView):

     def post(self, request):
        # mobile number and temprorilly password that has been sent to user via sms in signup view is given by user
        email = request.data.get("email")
        temp_password = request.data.get("temp_password")
        mobile = request.data.get("mobile")
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