from places.models import Country , State , DialCode
from places.serializers import CountrySerializer , StateSerializer , DialCodeSerializer
import json
def post(self , request):
    f = open('states.json' , encoding = 'utf-8')
    data = json.load(f)
    for item in data:
        country = Country.objects.filter(code = item['country_code']).first()    
        if country:
            state_dict = {'country' : country.id , 'ename' : item['ename' ], 'fname': item['fname']}
            serializer = StateSerializer(data = state_dict , many = False)
            if serializer.is_valid(raise_exception = True):
                serializer.save()
            state = State.objects.all()
        else:
            pass
    return Response(serializer.data, status=200)