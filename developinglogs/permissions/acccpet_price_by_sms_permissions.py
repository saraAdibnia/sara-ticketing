from os import dup
from unittest import result
from black import re
from django.http import response
from rest_framework import permissions
from order.models import  Waybill, waybill
from user.models import User
from developinglogs.models import ReceivedSms
from icecream import ic
##### Export #####
class IsWaybillOwnerBySMS(permissions.BasePermission):
    """ checking if sms is send by the owner of waybill and also the messageid is not duplicate"""

    def has_permission(self, request, view):
        duplicate = ReceivedSms.objects.filter(messageid = request.data.get('messageid')).exists()
        waybill_onwer = Waybill.objects.get(code = 'OIM'+request.data.get('message').replace(' ','').split('*')[0]).user
        ic(waybill_onwer)
        print('this is the result *********** \n', result)
        sender = User.objects.filter(mobile = '98'+request.data.get('from')[1:])
        return waybill_onwer in sender and not duplicate 


