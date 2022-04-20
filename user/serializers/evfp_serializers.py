from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth.hashers import make_password
# from drf_extra_fields import geo_fields

from user.models import User, Captcha, EVFP





class EVFPSerializer(ModelSerializer):

    class Meta:
        model = EVFP
        fields = '__all__'