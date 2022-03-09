from rest_framework.test import APIClient, APITestCase
from user.models import UserProfile, UserLocation, UserBankAccount, LegalUserInfo

class UserBankAccountInfoTestCase(APITestCase):

    def setUp(self):

        user = UserProfile.objects.create_user(
            mobile='09125351125',
            role=0,
            password='simplepass'
        )
        self.client = APIClient()

        login_url = '/user/login/'
        login_req = {
            "username": '09125351125',
            'password': 'simplepass'
        }
        login_response = self.client.post(login_url, login_req)
        token = login_response.data.get('Authorization')

        self.client.credentials(HTTP_AUTHORIZATION = token)


    def test_bank_account_view_empty(self):
        
        #test empty
        url = '/user/bank_account_info/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.data.get('succeeded'))


    def test_bank_account_create(self):
        
        #create
        url = '/user/bank_account_info/'
        req = {
            "bank_account_number":"128790",
            "bank_name": "سامان",
            "debit_card_number": "6291 - 2198 - 2399 - 1312",
            "sheba_number": "IR123123123123123",
            "branch_name": "پیروزی",
            "branch_code": "21"
        }
        response = self.client.post(url, req)

        #test create
        self.assertTrue(response.data.get('succeeded'))
        self.assertEqual(response.status_code, 200)



    def test_bank_account_view(self):

        #create
        url = '/user/bank_account_info/'
        req = {
            "bank_account_number":"128790",
            "bank_name": "سامان",
            "debit_card_number": "6291 - 2198 - 2399 - 1312",
            "sheba_number": "IR123123123123123",
            "branch_name": "پیروزی",
            "branch_code": "21"
        }
        response = self.client.post(url, req)


        #retreive test
        url1 = '/user/bank_account_info/'
        response1 = self.client.get(url1)
        self.assertEqual(response1.status_code, 200)
        self.assertTrue(response1.data.get('succeeded'))
        self.assertEqual(response1.data.get('user_bank_account')['bank_account_number'], "128790")
        self.assertEqual(response1.data.get('user_bank_account')['bank_name'], "سامان")
        self.assertEqual(response1.data.get('user_bank_account')['debit_card_number'], "6291 - 2198 - 2399 - 1312")
        self.assertEqual(response1.data.get('user_bank_account')['sheba_number'], "IR123123123123123")
        self.assertEqual(response1.data.get('user_bank_account')['branch_name'], "پیروزی")
        self.assertEqual(response1.data.get('user_bank_account')['branch_code'], "21")

        
        
    def test_bank_account_change(self):
        #create
        url = '/user/bank_account_info/'
        req = {
            "bank_account_number":"128790",
            "bank_name": "سامان",
            "debit_card_number": "6291 - 2198 - 2399 - 1312",
            "sheba_number": "IR123123123123123",
            "branch_name": "پیروزی",
            "branch_code": "21"
        }
        response = self.client.post(url, req)

        #change
        url2 = '/user/bank_account_info/'
        req2 = {
            "bank_account_number":"1",
            "bank_name": "2",
            "debit_card_number": "3",
            "sheba_number": "4",
            "branch_name": "5",
            "branch_code": "6"
        }
        response2 = self.client.post(url2, req2)

        #check change
        url1 = '/user/bank_account_info/'
        response1 = self.client.get(url1)
        self.assertEqual(response1.status_code, 200)
        self.assertTrue(response1.data.get('succeeded'))
        self.assertEqual(response1.data.get('user_bank_account')['bank_account_number'], "1")
        self.assertEqual(response1.data.get('user_bank_account')['bank_name'], "2")
        self.assertEqual(response1.data.get('user_bank_account')['debit_card_number'], "3")
        self.assertEqual(response1.data.get('user_bank_account')['sheba_number'], "4")
        self.assertEqual(response1.data.get('user_bank_account')['branch_name'], "5")
        self.assertEqual(response1.data.get('user_bank_account')['branch_code'], "6")