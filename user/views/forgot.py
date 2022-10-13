from user.serializers.user_serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from user.my_authentication.aseman_token_auth import MyToken
from utilities import validation_error, existence_error
from rest_framework import status
import uuid
from django.utils import timezone
from user.serializers import UserSerializer, EVFPSerializer
from user.models import User, EVFP
from extra_scripts.send_sms import send_sms
from developinglogs.models.sms_log_models import SmsCategory
from extra_scripts.emailnormalization import normalize_email

class ForgotPassByEmailAvailability(APIView):

    """by this root the front end can understand that forgot pass with email is an option or not"""

    def post(self, request):

        user_obj = User.objects.filter(
            mobile=request.data.get("mobile")).first()
        if not user_obj:
            return existence_error("user")

        if user_obj.email_verified:
            return Response({"succeeded": True}, status=200)
        else:
            return Response({"succeeded": False}, status=200)


class ForgotPassView(APIView):
    """
    This view is used for sending disposable code for users to login when they have forgotten their password
    """

    def post(self, request):
        """
        after sending a request including user's mobile num to this method, succeeded would turn out true and then
        front-end should call login api with this mobile phone and the disposable password that has been asked from user to look from their sms.
        """

        # generating for digit random int number for code
        code = str(uuid.uuid4().int)[:5]

        # finding user by filtering their mobile num
        mobile = request.data.get("mobile")
        user_obj = User.objects.filter(mobile=mobile).first()
        if not user_obj:
            return existence_error("user")

        # changing user temperory password with code that was generated above
        user_serialized = UserSerializer(
            user_obj, data={"temp_password": make_password(code)}, partial=True
        )
        if not user_serialized.is_valid():
            return validation_error(user_serialized)
        user_serialized.save()

        #sending the code to user using kavenegar (sendpassword template) ==> take a look at company's account in kavenegar website
        # sms_text = 'مشتری گرامی رمز فراموشی یک بار مصرف شما: {} A.S.P'.format(
        #     code)
        # send_sms(request.data.get('mobile'), sms_text,
        #          '100045312', 1, request.user.id)
        # smsCategory_obj = SmsCategory.objects.filter(code=3).first()
        # print(f"smsCategory_obj {smsCategory_obj.isActive}")
        # if smsCategory_obj.isActive == True:
        #     sms_text = smsCategory_obj.smsText.format(code)
        #     send_sms(
        #         user_obj.mobile,
        #         sms_text,
        #         smsCategory_obj.id,
        #         smsCategory_obj.get_sendByNumber_display(),
        #         request.user.id,
        #     )

        res = {"succeeded": True, "code": code}

        return Response(res, status=200)

    def patch(self, request):
        """
        after sending a request including user's email to this method, succeeded would turn out true and then
        front-end should call login api with this email and the disposable password that has been asked from user to look from their email.
        """

        # retreving the user with email provided
        user_obj = User.objects.filter(
            mobile=request.data.get("mobile")).first()
        if not user_obj:
            return existence_error("user")

        # if not user_obj.email:
        #     response_json = {
        #         "succeeded": False,
        #         "details": "User with this mobile number has not registered email",
        #     }
        #     return Response(response_json, status=405)

        # elif not user_obj.email_verified:
        #     response_json = {
        #         "succeeded": False,
        #         "details": "Email not verified. forgot pass by email is not available",
        #     }
        #     return Response(response_json, status=405)

        # generating for digit random int number for code
        code = str(uuid.uuid4())

        EVFP_serialized = EVFPSerializer(
            data={"user": request.user.id, "code": code})
        if not EVFP_serialized.is_valid():
            return validation_error(EVFP_serialized)
        EVFP_serialized.save()

        # url_address = "http://localhost:3000/forgot_pass/{}".format(code)

        # configurating and sending an email to user including the disposable password.
        subject, from_email, to = (
            "بازیابی رمز عبور",
            "test@asemanexpress.com",
            normalize_email(user_obj.email),
        )
        text_content = "Forgot password."

        sr = '<html> <head> <meta http-equiv="Content-Type" content="text/html; charset=uf8" /> </head>  <body style="text-align: center ;">  <img src="https://asemanexpress.com/wp-content/uploads/2020/06/h-logo.png" style="width: 248px; height: 106px" />  <h1>Password Reset</h1>  <p>It seems that you have forgot your password to enter ASP web service. Temporary password to enter is provided below<p>  <p>:به نظر می‌رسد شما رمز عبور ورود به وبسایت آسمان سوی پارسیان را فراموش کرده‌اید. بلا کلیک بر روی لینک زیر می‌توانید یک رمز عبور جدید برای خود تعریف کنید </p> <form action={0}> <input style="background:none; border:none; color:#fff; margin-top:1rem; width:200px ; padding: 2rem ;background: #383030 ; color: aliceblue ; display: block ; margin: auto; border-radius: 20px ; text-align: center" type="submit" value="فراموشی رمز عبور" /></form> <p>If you did not request for this, you can safely ignore this email.<p><p> .اگر شما درخواست فراموشی رمز عبور نداده‌اید، به سادگی از این ایمیل صرف نظر کنید. </p> <p>We love hearing from you.</p> <p> Aseman Sooye Parsian, Vahabi Barzi valley, 16th st., Ghanbarzade, Beheshti st., Tehran, Iran. </p> <p>Phone number: +9821-45312</p> <p>Email Address: info@asemanexpress.com</p> </body> </html>'.format(
            url_address
        )
        html_content = sr.format(code)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        response_json = {"succeeded": True, "email": user_obj.email}
        return Response(response_json, status=200)


class ForgotPassEmailCallBack(APIView):
    def post(self, request):
        """by sending the code which was delivered in post view to user's email, user can change their email status to verified"""
        EVFP_obj = EVFP.objects.filter(code=request.data.get("code")).first()
        if not EVFP_obj:
            return existence_error("evfp")

        else:

            user_obj = User.objects.filter(id=EVFP_obj.user.id).first()
            if not user_obj:
                return existence_error("user")

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

            token, created = MyToken.objects.get_or_create(user=user_obj)

            user_serialized = UserSerializer(
                user_obj,
                data={"needs_to_change_pass": True,
                      "last_login": timezone.now()},
                partial=True,
            )
            if not user_serialized.is_valid():
                return validation_error(user_serialized)
            user_serialized.save()

            EVFP_obj.delete()

            response_json = {
                "succeeded": True,
                "Authorization": "Token {}".format(token.key),
                "role": user_obj.role,
            }

            return Response(response_json, status=200)


class ForgotPassSMSCallBack(APIView):
    def post(self, request):

        # finding user
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
            token, created = MyToken.objects.get_or_create(user=user_obj)

            # user should change their password if they login successfuly via this method. so:
            if user_obj.role == 0:
                user_serialized = UserSerializer(
                    user_obj,
                    data={
                        "needs_to_change_pass": True,
                        "temp_password": None,
                        "last_login": timezone.now(),
                    },
                    partial=True,
                )
            else:
                user_serialized = UserSerializer(
                    user_obj,
                    data={"temp_password": None, "last_login": timezone.now()},
                    partial=True,
                )

            if not user_serialized.is_valid():
                return validation_error(user_serialized)
            user_serialized.save()

            # successful login
            response_json = {
                "succeeded": True,
                "Authorization": "Token {}".format(token.key),
                "role": user_obj.role,
            }

            return Response(response_json, status=200)

        # if the password is wrong
        else:
            response_json = {
                "succeeded": False,
                "details": "Wrong Password. Permission Denied.",
            }
            return Response(response_json, status=403)

    def patch(self, request):
        user_mobile = request.data.get("mobile")

        new_pass = request.data.get("pass")

        user_obj = User.objects.filter(mobile=user_mobile).first()

        user_obj.set_password(new_pass)
        user_obj.save()

        response_json = {
            "succeeded": True,
        }
        return Response(response_json, status=200)
