from datetime import datetime
from developinglogs.models.sms_log_models import SmsSend

from django.utils.timezone import make_aware
from celery import app

from extra_scripts.kavenegar import *
from developinglogs.models import SMSLog
from developinglogs.serializers import SMSLogSerializer
from extra_scripts.EMS import (
    validation_error,
)
from celery import shared_task
from icecream import ic


# @shared_task
def send_sms(receptor, message, smsCategoryCode, sender="100045312", user=None): #TODO rename the smsCategoryCode to sms_cat_id
    # sms_send_or_not = SmsSend.objects.filter(kind=kind).first().is_send
    print(f')))))))))))))))))))))))))))))))))))))))))){smsCategoryCode}')

    # if sms_send_or_not == True:
    #     pass
    # else:
    #     return 0

    try:
        import json
    except ImportError:
        import simplejson as json
    try:
        api = KavenegarAPI(
            "58546C51517035384E664B44345970343258654E2F5132383555714C69437876616358682B6B444E777A673D"
        )

        params = {
            "receptor": str(receptor),
            "message": message,
            "sender": str(sender),
        }

        response = api.sms_send(params)
        status = response["return"]["status"]

        if int(status) == 200:
            ic()

            req = {
                "params_receptor": str(receptor),
                "params_message": message,
                "params_sender": str(sender),
                "validation": False,
                "status": response["return"]["status"],
                "message": response["return"]["message"],
                "messageid": response["entries"][0]["messageid"],
                "message": response["entries"][0]["message"],
                "status": response["entries"][0]["status"],
                "statustext": response["entries"][0]["statustext"],
                "sender": response["entries"][0]["sender"],
                "receptor": response["entries"][0]["receptor"],
                "date": make_aware(
                    datetime.fromtimestamp(
                        float(response["entries"][0]["date"]))
                ),
                "smsCat": smsCategoryCode,
                "cost": response["entries"][0]["cost"],
                "send_by": user,
                "is_sending": True,
            }
        else:
            ic()
            req = {
                "status": response["return"]["status"],
                "message": response["return"]["message"],
            }


        sms_logs_serialized = SMSLogSerializer(data=req)
        if not sms_logs_serialized.is_valid():
            return validation_error(sms_logs_serialized)
        sms_logs_serialized.save()

        # #developing issues
        # 400
        # 412
        # 413

        # #kavenegar account issues
        # 401
        # 403
        # 418
        # 505

        # #unsuccess
        # 402

        # #try again
        # 409

        # #invalid receptor
        # 411

        # # others
        # 414
        # 417
        # 419
        # 502
        # 503
        # 504
        # 506
        # 507
        # 601
        # 602
        # 603

    except HTTPException as e:
        ic()
        print(str(e))
