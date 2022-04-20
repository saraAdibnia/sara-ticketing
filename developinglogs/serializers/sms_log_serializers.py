from rest_framework.serializers import ModelSerializer
from user.serializers import UserSerializer
from developinglogs.models import *




class SMSLogShowSerializer(ModelSerializer):
    send_by = UserSerializer()

    class Meta:
        model = SMSLog
        fields = "__all__"


class SmsCategorySerializer(ModelSerializer):
    class Meta:
        model = SmsCategory
        fields = "__all__"

class SMSLogSerializer(ModelSerializer):
    class Meta:
        model = SMSLog
        fields = "__all__"
class SMSLogShowSerializer(ModelSerializer):
    smsCat = SmsCategorySerializer()
    class Meta:
        model = SMSLog
        fields = "__all__"

class ReceivedSmsSerializer(ModelSerializer):
    class Meta:
        model = ReceivedSms
        fields = "__all__"
