from rest_framework.test import APIClient, APITestCase
from django.contrib.gis.geos import Point

from user.models import UserProfile, UserLocation, UserBankAccount, LegalUserInfo


class UserLocationManagementTestCase(APITestCase):
    '''we are trying to manage data in user location '''
    def setUp(self):
        '''we create a user and user location object'''
        user1 = UserProfile.objects.create_user(
                            mobile='09125351125', 
                            password='simplepass', 
                            temp_password='1234'
                            )

        user_location = UserLocation.objects.create(
            user=user1, 
            default=True, 
            address_name='محل کار', 
            full_name='سپهر محمدی',
            uni_code='12123131',
            mobile='0912324324',
            address_text='وهابی برزی', 
            phone='45312', 
            postal_code='postal12', 
            description='اینجا محل کار من است', 
            location = Point(1,1)
            )

    def test_creatting_new(self):
        '''in this test case we are trying to add a new user location to the user that is created in setUp'''
        self.client = APIClient()
        #logging in the user to get authentication credentials
        login_url = '/user/login/'
        login_req = {
            "username": '09125351125',
            'password': 'simplepass'
        }
        #
        login_response = self.client.post(login_url, login_req)
        token = login_response.data.get('Authorization')

        url = '/user/address/'
        self.client.credentials(HTTP_AUTHORIZATION = token)

        req = {
            "address_name": 'منزل',
            "address_text": 'عباس آباد',
            "phone": '1212',
            "postal_code": '1213',
            "location": {
                "longitude":1,
                "latitude": 1,
            },
            "description": 'این آدرس خانه است.',
            "real": True,
            "default": True,
        }
        response = self.client.post(url, req, format='json')
        user_location_obj = UserLocation.objects.last()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get('succeeded'))
        self.assertEqual(user_location_obj.address_name, 'منزل')
        self.assertEqual(user_location_obj.address_text, 'عباس آباد')
        self.assertEqual(user_location_obj.phone, '1212')
        self.assertEqual(user_location_obj.postal_code, '1213')
        self.assertEqual(user_location_obj.description, 'این آدرس خانه است.')
        self.assertFalse(user_location_obj.default)
        # self.assertEqual(Point(1,1), user_location_obj.location)

    def test_viewing_address_list(self):

        #can add details to this test 
        
        self.client = APIClient()

        login_url = '/user/login/'
        login_req = {
            "username": '09125351125',
            'password': 'simplepass'
        }
        login_response = self.client.post(login_url, login_req)
        token = login_response.data.get('Authorization')

        url = '/user/address_list/'
        self.client.credentials(HTTP_AUTHORIZATION = token)
        


        response = self.client.post(url)
        self.assertTrue(response.data.get('succeeded'))
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data.get('user_locations')[0].get('default'), True)
        # self.assertEqual(response.data.get('user_locations')[0].get('address_name'), 'محل کار')
        # self.assertEqual(response.data.get('user_locations')[0].get('address_text'), 'وهابی برزی')
        # self.assertEqual(response.data.get('user_locations')[0].get('phone'), '45312')
        # self.assertEqual(response.data.get('user_locations')[0].get('postal_code'), 'postal12')
        # self.assertEqual(response.data.get('user_locations')[0].get('description'), 'اینجا محل کار من است')

    def test_changing_default(self):
        self.client = APIClient()

        login_url = '/user/login/'
        login_req = {
            "username": '09125351125',
            'password': 'simplepass'
        }
        login_response = self.client.post(login_url, login_req)
        token = login_response.data.get('Authorization')

        url = '/user/address/'
        self.client.credentials(HTTP_AUTHORIZATION = token)
        req = {
            "user_location_id": UserLocation.objects.first().id
        }
        response = self.client.patch(url, req)

        self.assertTrue(response.data.get('succeeded'))
        self.assertEqual(response.status_code, 200)
    
    def test_delete(self):
        self.client = APIClient()

        login_url = '/user/login/'
        login_req = {
            "username": '09125351125',
            'password': 'simplepass'
        }
        login_response = self.client.post(login_url, login_req)
        token = login_response.data.get('Authorization')

        url = '/user/address/'
        self.client.credentials(HTTP_AUTHORIZATION = token)
        req = {
            "user_location_id": UserLocation.objects.first().id
        }
        response = self.client.delete(url, req)

        self.assertTrue(response.data.get('succeeded'))
        self.assertEqual(response.status_code, 200)

    def test_address_details(self):

        self.client = APIClient()

        login_url = '/user/login/'
        login_req = {
            "username": '09125351125',
            'password': 'simplepass'
        }
        login_response = self.client.post(login_url, login_req)
        token = login_response.data.get('Authorization')

        url = '/user/address_details/'
        self.client.credentials(HTTP_AUTHORIZATION = token)
        req = {
            "id": UserLocation.objects.first().id
        }
        response = self.client.post(url, req)
        self.assertTrue(response.data.get('succeeded'))
        self.assertEqual(response.status_code, 200)
    
    def test_default_view(self):

        self.client = APIClient()

        login_url = '/user/login/'
        login_req = {
            "username": '09125351125',
            'password': 'simplepass'
        }
        login_response = self.client.post(login_url, login_req)
        token = login_response.data.get('Authorization')

        url = '/user/address_list/'
        self.client.credentials(HTTP_AUTHORIZATION = token)
        req = {
            "id": UserLocation.objects.first().id
        }
        response = self.client.patch(url, req)
        self.assertTrue(response.data.get('succeeded'))
        self.assertEqual(response.status_code, 200)