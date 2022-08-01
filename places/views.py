from places.models import  City, State, Country, DialCode
from places.serializers import DialCodeSerializer ,CountrySerializer , CitySerializer , StateSerializer , ShowCountrySerializer
from rest_framework.response import Response
from extra_scripts.EMS import existence_error , validation_error
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
class DialCodeView(APIView):
    """by sending dial_code with this format "+98" to this view you can retreive country name and flag emoji"""

    def get(self, request):

        dial_code_objs = DialCode.objects.all()

        dial_code_serialized = DialCodeSerializer(dial_code_objs, many=True)

        response_json = {"succeeded": True, "dial_codes": dial_code_serialized.data}

        return Response(response_json, status=200)

class CityView(APIView):
    """by sendin state id to this view you will retreive cities of the country"""

    def post(self, request):

        city_objs = City.objects.filter(state=request.data.get("state_id"))

        city_serialized = CitySerializer(city_objs, many=True)

        response_json = {"succeeded": True, "cities": city_serialized.data}

        return Response(response_json, status=200)

    def patch(self, request):

        city_objs = City.objects.filter(state__country=request.data.get("country_id"))

        city_serialized = CitySerializer(city_objs, many=True)

        response_json = {"succeeded": True, "cities": city_serialized.data}
        return Response(response_json, status=200)

class CountryView(APIView):
    """retreiveing countries in the world"""

    def get(self, request):
        """by only calling this method you will retreive all countries in the world"""

        #### Filter result
        allowed_filters = (
            "fname__icontains",
            "ename__icontains",
        )
        kwargs = {}
        for key, value in request.query_params.items():
            if key in allowed_filters:
                kwargs.update({key: value})

        country_objs = Country.objects.filter(**kwargs).order_by("fname")

        country_serialized = ShowCountrySerializer(country_objs, many=True)

        response_json = {"succeeded": True, "countries": country_serialized.data}

        return Response(response_json, status=200)

  
    def post(self, request):
        """by sending country id, you will retreive that country details"""

        country_obj = Country.objects.get(id=request.data.get("id"))
        country_serialized = CountrySerializer(country_obj)

        response_json = {"succeeded": True, "zones": country_serialized.data}

        return Response(response_json, status=200)

    def patch(self, request):
        """edit country zone"""
        country_obj = Country.objects.filter(id=request.data.get("id")).first()
        if not country_obj:
            return existence_error("country")

        country_serialized = CountrySerializer(
            country_obj,
            data={"zone": request.data.get("zone")},
            partial=True,
        )
        if not country_serialized.is_valid():
            return validation_error(country_serialized)
        country_serialized.save()

        request.data.update({"country": country_obj.id})

        response_json = {
            "succeeded": True,
        }
        return Response(response_json, status=200)



class StateView(APIView):
    """by sending country id to this view you will retreive states of the country"""
    #
    permission_classes = []

    def post(self, request):

        state_objs = State.objects.filter(country=request.data.get("country_id")).order_by('fname')

        state_serialized = StateSerializer(state_objs, many=True)

        response_json = {"succeeded": True, "states": state_serialized.data}

        return Response(response_json, status=200)

class CreateStateView(CreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
