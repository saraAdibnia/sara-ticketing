from rest_framework.test import APIClient, APITestCase

from developinglogs.models import SMSLog


class SMSLogModelTestCase(APITestCase):

    def setUp(self):

        sms_log = SMSLog.objects.create(
            params_receptor
params_message
params_sender
status
message
messageid
message
status
statustext
sender
receptor
date
cost
        )

    def test_sms_logs_model(self):