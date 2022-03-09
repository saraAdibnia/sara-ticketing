#In this tests we are going to check the login proccess of user through all different options available for him/her
#Also Error Management of user login is being tested afterwards
from rest_framework.test import APIClient, APITestCase

from user.models import *
from user.serializers import *

from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token


class UserNormalLoginCase(APITestCase):
    """Checking different scenarios of user logging in"""

    def setUp(self):
        """we create a user with fields shown below, in order to check the login proccess"""
        user1 = UserProfile.objects.create_user(
                                        mobile="09125351125", 
                                        password='thisisasimplepassword', 
                                        )
        user2 = UserProfile.objects.create_user(
                                        mobile="093094328060", 
                                        password='pass',
                                        role=1, 
                                        )
    def test_successful_login_with_username(self):
        """correct mobile and password scenario"""

        url = '/user/login/'
        self.client = APIClient()

        req = {
            'username': '09125351125',
            'password': 'thisisasimplepassword'
        }

        response = self.client.post(url, req)
        #the status code should be 200 and succeeded must be true
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('succeeded'), True)
        #checks wether the returned token in api's response is the one saved in the database for user or not
        self.assertEqual(response.data.get('Authorization').split()[1], Token.objects.filter(user_id=UserProfile.objects.filter(mobile='09125351125').first().id).first().key)


    def test_wrong_password(self):
        """right username or mobile, providing wrong password (permission denied) scenario"""

        url = '/user/login/'
        self.client = APIClient()

        #making some request jsons including wrong main password or disposable password
        req = {
            'username': '09125351125',
            'password': 'badpass'
        }

        #saving the response in all methods of logging in
        response = self.client.post(url, req)

        # in all three methods of loging in the status code should be returned as 403 forbidden
        self.assertEqual(response.status_code, 403)

    def test_existence_error(self):
        """user with this credentials does not exist"""

        url = '/user/login/'
        self.client = APIClient()

        #making some request jsons including not existing user cred
        req = {
            'username': '09125351123',
            'password': 'pass'
        }

        #saving the response in all methods of logging in
        response = self.client.post(url, req)

        # in all three methods of loging in the status code should be returned as 403 forbidden
        self.assertEqual(response.status_code, 404)

    def test_role_error(self):
        """user is not a simple user and should go through corporate login"""
        url = '/user/login/'
        self.client = APIClient()

        #making some request jsons including not simple user creds
        req = {
            'username': '093094328060',
            'password': 'pass'
        }

        #saving the response in all methods of logging in
        response = self.client.post(url, req)
        self.assertEqual(response.status_code, 400)

    def test_not_provided(self):
        """authentication credentials not provided"""
        url = '/user/login/'
        self.client = APIClient()

        #making some request jsons including not simple user creds
        req = {
            'username': '09125351125',
        }

        req1 = {
            'password': 'pass'
        }

        response = self.client.post(url, req)
        response1 = self.client.post(url, req1)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response1.status_code, 401)

    def test_not_active(self):
        pass




class ForgotPasswordTestCase(APITestCase):
    """we create a user and check both ways to get a disposable code for login"""
    def setUp(self):
        user1 = UserProfile.objects.create_user(
                            role=0,
                            email='soheildsh@gmail.com',
                            password='thisisasimplepassword', 
                            temp_password="1234", 
                            mobile="09125351125",
                            email_verified=True,
                            )
                            
        user2 = UserProfile.objects.create_user(
            role=0,
            mobile='093094328060',
            password='simplepass',
        )

    def test_sms(self):
        """after calling this root, user should provide mobile and pass to login api"""
        # sending user mobile number to forgotpass root
        url = '/user/forgotpass/'
        req = {
            "mobile": "09125351125"
        }

        self.client = APIClient()
        #post method is there to send disposable code via sms
        response = self.client.post(url, req)

        #check that everythin went ok
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get('succeeded'))

    def test_not_saved_or_not_verified_email(self):
        #sending user mobile to forgot pass root
        url = '/user/forgotpass/'
        req = {
            "mobile": "093094328060"
        }
        self.client = APIClient()
        #patch method is there for sending disposable code to user's email
        response = self.client.patch(url, req)

        #check that everything is ok
        self.assertEqual(response.status_code, 405)
        self.assertFalse(response.data.get('succeeded'))

    def test_email(self):
        """after calling this root, user should provide email and pass to login api"""

        #sending user mobile to forgot pass root
        url = '/user/forgotpass/'
        req = {
            "mobile": "09125351125"
        }

        self.client = APIClient()
        #patch method is there for sending disposable code to user's email
        response = self.client.patch(url, req)

        #check that everything is ok
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get('succeeded'))
