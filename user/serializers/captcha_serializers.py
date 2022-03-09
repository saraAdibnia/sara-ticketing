from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth.hashers import make_password
# from drf_extra_fields import geo_fields

from user.models import UserProfile,Captcha, EVFP


class CaptchaSerializer(ModelSerializer):

    class Meta:
        model = Captcha
        fields = '__all__'

