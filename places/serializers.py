from sre_parse import State
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from places.models import (
    City,
    State,
    Country,
    DialCode,
)
class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class CitySerializer(ModelSerializer):

    class Meta:
        model = City
        fields = "__all__"

class StateSerializer(ModelSerializer):

    class Meta:
        model = State
        fields = "__all__"


class ShowCountrySerializer(ModelSerializer):
    """simple country serializer"""
    class Meta:
        model = Country
        fields = '__all__'


class ShowCitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

class ShowStateSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"


class DialCodeSerializer(ModelSerializer):
    class Meta:
        model = DialCode
        fields = "__all__"
