from developinglogs.models import ReceivedSms, SMSLog
from developinglogs.serializers import ReceivedSmsSerializer, SMSLogSerializer
from django.http import HttpRequest
# from elasticsearch import RequestError
from extra_scripts.EMS import existence_error, validation_error
# from httpx import request
from icecream import ic
# from operatorimport.models.propose_price_models import WaybillProposedPrice
# from operatorimport.serializers.propose_price_serializers import \
#     WaybillProposedPriceSerializer
# from order.models import ExportWaybill, Waybill
# from ordercustomer.views import PriceAcceptImportWaybillByUser
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import UserProfile
from developinglogs.permissions import IsWaybillOwnerBySMS

class SMSDeliveryCallBack(APIView):
    def post(self, request):

        sms_log_obj = SMSLog.objects.filter(
            messageid=request.data.get('messageid')).first()
        if not sms_log_obj:
            return existence_error('sms')

        sms_log_serialized = SMSLogSerializer(
            sms_log_obj,
            data={
                "status": request.data.get('status'),
            },
            partial=True
        )
        if not sms_log_serialized.is_valid():
            return validation_error(sms_log_serialized)
        sms_log_serialized.save()

        return Response({"succeeded": True}, status=200)


class ReceivedSmsViews(generics.CreateAPIView):
    """handling received sms and accpeting import waybill by sms"""

    serializer_class = ReceivedSmsSerializer 
    queryset = ReceivedSms.objects.filter() 
    permission_classes = [IsWaybillOwnerBySMS]

    # def user_accept_import_waybill(self, message, user =None ):
    #     """"using PriceAcceptImportWaybillByUser view to update the status of proposed price of an import waybill """

    #     wb = Waybill.objects.get(code = 'OIM'+message.split('*')[0] ) 
    #     acceept = '1' == message.replace(' ','').split('*')[1]
    #     proposed_price_obj = WaybillProposedPrice.objects.filter(waybill = wb).last()
    #     # create a request to use the view for accepting by customer
    #     new_request = HttpRequest()
    #     new_request.user = user
    #     new_request.method = "POST"
    #     new_request.data = {'proposed_price': proposed_price_obj.id, 'id': wb.id, 'accept': acceept }
    #     r = PriceAcceptImportWaybillByUser.post(self, request=new_request)
    #     status_data = r.data
    #     # if the process of accepting is not ok we just ignore it.
    #     return None

    def create(self, request, *args, **kwargs):
        """create a received sms object """
        ic()
        request.data._mutable=True
        request.data['from'] = '98'+request.data.get('from')[1:]
        try: 
            owner = UserProfile.objects.filter(mobile = request.data.get('from') ).last()
            request.data['sender_user'] = owner.id
        except:
            owner = None
            pass

        request.data['sender'] = request.data.get('from')
        request.data['receptor'] = request.data.get('to')
        request.data['message'] = request.data.get('message')
        request.data['messageid'] = request.data.get('messageid')
        
        if '*' in  request.data.get('message'): # if * in message body it is for accepting import price by user
            self.user_accept_import_waybill(request.data.get('message'), owner ) 
        
        return super().create(request, *args, **kwargs)
