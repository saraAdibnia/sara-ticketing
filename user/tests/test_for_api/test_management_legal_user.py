from rest_framework.test import APIClient, APITestCase

from user.models import UserProfile, LegalUserInfo
from places.models import City, State, Country


class LegalUserViewTestCase(APITestCase):

    def setUp(self):

        user = UserProfile.objects.create_user(
            mobile='09125351125',
            password='coolpass',
            is_real=False
        )

        country = Country.objects.create(
            ename='Iran'
        )
        state = State.objects.create(
            ename='Tehran'
        )
        city = City.objects.create(
            ename="Tehran"
        )

    def test_legal_user_no_legal_info(self):

        self.client = APIClient()

        #logging in the user to get authentication credentials
        login_url = '/user/login/'
        login_req = {
            "username": '09125351125',
            'password': 'coolpass'
        }
        login_response = self.client.post(login_url, login_req)
        token = login_response.data.get('Authorization')
        self.client.credentials(HTTP_AUTHORIZATION = token)

        url = '/user/profile/'
        response = self.client.get(url)


        self.assertFalse(response.data.get('user')['legal_user_info']['company_name'])

    def test_legal_user_info_create_and_change(self):
        
        self.client = APIClient()

        #logging in the user to get authentication credentials
        login_url = '/user/login/'
        login_req = {
            "username": '09125351125',
            'password': 'coolpass'
        }
        login_response = self.client.post(login_url, login_req)
        token = login_response.data.get('Authorization')
        self.client.credentials(HTTP_AUTHORIZATION = token)

        #creatting legal user info
        url = '/user/legal_info/'
        req = {
            "company_name": "آسمان",
            "economic_code": "1221",
            "national_id": "1222",
            "registration_id": "1223",
            "register_date": "2020-10-12",
            "postal_code": "1224",
            "address_text": "خیابان",
            "country": Country.objects.first().id,
            "state": State.objects.first().id,
            "city": City.objects.first().id,
            "email": "soheildsh@gmail.com",
            "phone": "1225",
            "field_of_work": "زمینه کاری",
        }

        response = self.client.post(url, req)
        self.assertTrue(response.data.get('succeeded'))
        self.assertEqual(response.status_code, 200)
        

        #checking profile
        profile_url = '/user/profile/'
        profile_response = self.client.get(profile_url)

        self.assertEqual(profile_response.data.get('user')['legal_user_info']['company_name'], 'آسمان')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['economic_code'], '1221')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['national_id'], '1222')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['registration_id'], '1223')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['register_date'], '2020-10-12')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['postal_code'], '1224')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['address_text'], 'خیابان')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['country']['id'], 1)
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['state']['id'], 1)
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['city']['id'], 1)
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['email'], 'soheildsh@gmail.com')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['phone'], '1225')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['field_of_work'], 'زمینه کاری')

        #change legal info
        req2 = {    
            "company_name": "آسمان سوی پارسیان",  #this field has changes and should be updated
            "economic_code": "1221",
            "national_id": "1222",
            "registration_id": "1223",
            "register_date": "2020-10-12",
            "postal_code": "1224",
            "address_text": "خیابان",
            "country": Country.objects.first().id,
            "state": State.objects.first().id,
            "city": City.objects.first().id,
            "email": "soheildsh@gmail.com",
            "phone": "1225",
            "field_of_work": "زمینه کاری",
        }

        response2 = self.client.post(url, req2)
        self.assertTrue(response2.data.get('succeeded'))
        self.assertEqual(response2.status_code, 200)


        #check legal info after changed
        profile_response = self.client.get(profile_url)

        self.assertEqual(profile_response.data.get('user')['legal_user_info']['company_name'], 'آسمان سوی پارسیان')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['economic_code'], '1221')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['national_id'], '1222')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['registration_id'], '1223')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['register_date'], '2020-10-12')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['postal_code'], '1224')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['address_text'], 'خیابان')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['country']['id'], 1)
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['state']['id'], 1)
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['city']['id'], 1)
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['email'], 'soheildsh@gmail.com')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['phone'], '1225')
        self.assertEqual(profile_response.data.get('user')['legal_user_info']['field_of_work'], 'زمینه کاری')