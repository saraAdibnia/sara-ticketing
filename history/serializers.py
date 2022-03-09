from rest_framework.serializers import ModelSerializer
from . models import User_log

from user.serializers import (
    UserPermSerializer,
  UserProfileSimpleSerializer,
)


class UserLogSerializer(ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = User_log
        fields = "__all__"
