from rest_framework.serializers import ModelSerializer

from developinglogs.models import Mymodel

class MyModelSerializer(ModelSerializer):

    class Meta:

        model = Mymodel
        fields = '__all__'