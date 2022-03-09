from rest_framework.test import APIClient, APITestCase

from user.models import UserProfile, UserBankAccount

from datetime import datetime

class UserBankAccountTestCase(APITestCase):

    def setUp(self):

        user = UserProfile.objects.create_user(
            mobile="09125351125",
            password='simplepass'
        )

        user_bank_account = UserBankAccount.objects.create(
            user=UserProfile.objects.first(),
            bank_account_number='132123',
            bank_name='سامان',
            debit_card_number='72139123882132193',
            sheba_number='IR123123123123123123123',
            branch_name='میدان نیلوفر',
            branch_code='12313',
        )

        self.now = datetime.timestamp(datetime.now())

    def test_save_model(self):

        user_bank_account_obj = UserBankAccount.objects.first()

        self.assertEqual(user_bank_account_obj.user, UserProfile.objects.first())
        self.assertEqual(user_bank_account_obj.bank_account_number, '132123')
        self.assertEqual(user_bank_account_obj.bank_name, 'سامان')
        self.assertEqual(user_bank_account_obj.debit_card_number, '72139123882132193')
        self.assertEqual(user_bank_account_obj.sheba_number, 'IR123123123123123123123')
        self.assertEqual(user_bank_account_obj.branch_name, 'میدان نیلوفر')
        self.assertEqual(user_bank_account_obj.branch_code, '12313')
        self.assertTrue(user_bank_account_obj.created)
        self.assertTrue(user_bank_account_obj.modified)
