from rest_framework.test import APIClient, APITestCase
from user.models import *
from django.contrib.auth.hashers import check_password


class ChangePasswordTestCase(APITestCase):
    def setUp(self):

        user = UserProfile.objects.create_user(
            password='pass',
            email='soheildsh@gmail.com',
            mobile="09125351125",
            needs_to_change_pass=True
            )

        user2 = UserProfile.objects.create_user(
            password='pass',
            email='soheildsh@gmail.org',
            mobile="093094328060",
            needs_to_change_pass=False
            )

    # def test_mandatory_password_change(self):
    #     self.client = APIClient()
    #     #logging in the user to get authentication credentials
    #     login_url = '/user/login/'
    #     login_req = {
    #         "username": '09125351125',
    #         'password': 'pass'
    #     }
    #     login_response = self.client.post(login_url, login_req)
    #     token = login_response.data.get('Authorization')
        
    #     url = '/user/changepass'
    #     self.client.credentials(HTTP_AUTHORIZATION = token)
    #     req = {
    #         "password": 'anotherpass'
    #     }
    #     response = self.client.patch(url, req)

    #     self.assertTrue(response.data.get('succeeded'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(UserProfile.objects.filter(mobile='09125351125').first().check_password('anotherpass'))



    def test_reject_mandatory_password_change(self):
        
        self.client = APIClient()
        #logging in the user to get authentication credentials
        login_url = '/user/login/'
        login_req = {
            "username": '093094328060',
            'password': 'pass'
        }
        login_response = self.client.post(login_url, login_req)
        token = login_response.data.get('Authorization')

        url = '/user/changepass/'
        self.client.credentials(HTTP_AUTHORIZATION = token)
        req = {
            "password": 'anotherpass'
        }
        response = self.client.patch(url, req)
        self.assertFalse(response.data.get('succeeded'))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(UserProfile.objects.filter(mobile='093094328060').first().check_password('pass'))




    # def test_password_change(self):

    #     self.client = APIClient()
    #     #logging in the user to get authentication credentials
    #     login_url = '/user/login/'
    #     login_req = {
    #         "username": '093094328060',
    #         'password': 'pass'
    #     }
    #     login_response = self.client.post(login_url, login_req)
    #     token = login_response.data.get('Authorization')

    #     url = '/user/changepass'
    #     self.client.credentials(HTTP_AUTHORIZATION = token)
    #     req = {
    #         "old_password": "pass",
    #         "password": "anotherpass"
    #     }
    #     response = self.client.post(url, req)
    #     self.assertTrue(response.data.get('succeeded'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(UserProfile.objects.filter(username='soheildsh').first().check_password('anotherpass'))
    #     self.assertFalse(UserProfile.objects.filter(username='soheildsh').first().needs_to_change_pass)

