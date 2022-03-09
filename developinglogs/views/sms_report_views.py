
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime, timedelta
import requests


class SendList(APIView):

    def post(self, request):

        start_date = request.data.get('start_date')
        y, m, d = list(map(int, start_date.split('-')))
        start_date_unix_timestamp = datetime.timestamp(datetime(y, m, d))
        end_date_unix_timestamp = datetime.timestamp(
            datetime(y, m, d)+timedelta(days=1))

        request_data = {
            "startdate": start_date_unix_timestamp,
            "enddate": end_date_unix_timestamp
        }

        if request.data.get('sender'):
            request_data.update({"sender": request.data.get('sender')})

        list_url = 'https://api.kavenegar.com/v1/58546C51517035384E664B44345970343258654E2F5132383555714C69437876616358682B6B444E777A673D/sms/selectoutbox.json'
        list_response = requests.get(url=list_url, params=request_data)

        count_url = 'https://api.kavenegar.com/v1/58546C51517035384E664B44345970343258654E2F5132383555714C69437876616358682B6B444E777A673D/sms/countoutbox.json'
        count_response = requests.get(url=count_url, params=request_data)

        response_json = {
            "succeeded": True,
            "sms_list": list_response.json(),
            "sms_count": count_response.json()
        }

        return Response(response_json, status=200)
