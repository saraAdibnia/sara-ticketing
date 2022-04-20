from rest_framework.serializers import ModelSerializer
from . models import User_log

from user.serializers import (
    UserPermSerializer,
  UserSimpleSerializer,
)


class UserLogSerializer(ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = User_log
        fields = "__all__"
