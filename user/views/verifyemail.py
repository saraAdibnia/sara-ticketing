from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import uuid
from user.serializers import UserSerializer, EVFPSerializer
from user.models import UserProfile, EVFP
# from extra_scripts.EMS import *
from utilities import existence_error, validation_error

class VerifyEmailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        '''By calling this view if user has a registered email in their account a four digit code would be emailed to them in order to verify it'''

        user_obj = UserProfile.objects.filter(id=request.user.id).first()
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

            url_address = 'http://localhost:3000/verify_email/{}'.format(code)
            # sending new temp password to user
            subject, from_email, to = 'hello', 'test@asemanexpress.com', normalize_email(
                request.user.email)
            text_content = 'Verify Your Email'

            sr = '<html> <head> <meta http-equiv="Content-Type" content="text/html; charset=uf8" /> </head> <body style="text-align: center ;"> <img src="https://asemanexpress.com/wp-content/uploads/2020/06/h-logo.png" style="width: 248px; height: 106px" /> <h1>Email Verification</h1> <p>It seems that you want to verify your email in our website. Please click on the link below to do so:<p> <p>به نظر می‌رسد شما می‌خواهید ایمیل خود را در سامانه ما تایید کنید. برای انجام اینکار بر روی لینک زیر کلیک کنید: </p> <form action={}> <input style="background:none; border:none; color:#fff; margin-top:1rem; width:300px ; padding: 2rem ;background: #383030 ; color: aliceblue ; display: block ; margin: auto; border-radius: 20px ; text-align: center" type="submit" value="اعتبارسنجی ایمیل" /> </form> <p>If you did not request this you can safely ignore this email.<p> <p> .اگر شما درخواست نداده‌اید، به سادگی از این ایمیل صرف نظر کنید. </p> <p>We love hearing from you.</p> <p> Aseman Sooye Parsian, Vahabi Barzi valley, 16th st., Ghanbarzade, Beheshti st., Tehran, Iran. </p> <p>Phone number: +9821-45312</p> <p>Email Address: info@asemanexpress.com</p> </body> </html>'.format(
                url_address)

            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(sr, "text/html")
            msg.send()

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
        '''by sending the code which was delivered in post view to user's email, user can change their email status to verified'''
        EVFP_obj = EVFP.objects.filter(code=request.data.get('code')).first()
        if not EVFP_obj:
            return existence_error('evfp')

        else:

            user_obj = UserProfile.objects.filter(id=EVFP_obj.user.id).first()
            if not user_obj:
                return existence_error('user')

            user_serialized = UserSerializer(
                user_obj,
                data={
                    "email_verified": True,
                },
                partial=True
            )
            if not user_serialized.is_valid():
                return validation_error(user_serialized)
            user_serialized.save()

            EVFP_obj.delete()

            response_json = {
                "succeeded": True
            }

            return Response(response_json, status=200)
