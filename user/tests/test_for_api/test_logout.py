# In this test file we want to test our logout api located in /user/logout
# User Should be able to send his/her token in header to this api and delete it from our system
# no other data are used in body of request to logout
from rest_framework.test import APIClient, APITestCase
from user.models import *
from rest_framework.authtoken.models import Token


class LogoutCase(APITestCase):
    """test written to check proper logout"""

    def setUp(self):
        """we create a user to be able to send request from him"""
        self.user1 = UserProfile.objects.create_user(
            role=0,
            password='thisisasimplepassword',
            temp_password="1234",
            mobile="09125351125",
            email="soheildsh@gmail.com"
        )

    def test_successful_logout(self):
        """first we login the user to get the token and then we try to logout"""

        # trying to login using an APIClient
        url = '/user/login/'
        self.client = APIClient()

        req = {
            'username': '09125351125',
            'password': 'thisisasimplepassword'
        }
        response = self.client.post(url, req)
        # login completed and token created and received

        # tryin to logout using the same client
        url2 = '/user/logout/'
        # adding user auth credentials to header in order to logout
        self.client.credentials(
            HTTP_AUTHORIZATION=response.data.get('Authorization'))
        response2 = self.client.get(url2)

        # checking wether the logout was successful or not
        self.assertEqual(response2.data.get("succeeded"), True)
        self.assertEqual(response2.status_code, 200)
        # checking that wether the token is deleted or not
        self.assertEqual(Token.objects.filter(
            key=response.data.get('Authorization').split()[1]).first(), None)
