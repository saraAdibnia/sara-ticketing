#In this test case we are going to test signup of users.
from rest_framework.test import APIClient, APITestCase

from user.models import UserProfile, UserLocation, UserBankAccount, LegalUserInfo


class SignupCase(APITestCase):
    """we will check the different scenarios that may happen during user signup"""
    def setUp(self):
        """for test setup we create two users that one of them is an active user and another is not"""
        #active user
        user1 = UserProfile.objects.create_user(
            password="simplepass1",
            mobile="09125351125",
            email="soheil@gmail.com",
            is_active=True,
            is_real=True
            )

        #inactive user
        user2 = UserProfile.objects.create_user(
            password="simplepass2",
            mobile="093094328060",
            email="soheil@gmail.com",
            is_active=False,
            is_real=True
        )
    
    def test_user_exists(self):
        """we are trying to see everything works fine when user is trying to signup with data that are already used as another user's credentials"""

        req = {
            'password':"pass1",
            'mobile':"09125351125",    #record exist's with this mobile
            'email':"s@g.com",
        }

        url = '/user/signup/'
        self.client = APIClient()

        response = self.client.post(url, req)

        self.assertEqual(response.data.get('details'), 'user exists, please try to login')
        self.assertFalse(response.data.get('succeeded'))
        self.assertEqual(response.status_code, 406)

    def test_user_inactive(self):
        """
        now we are trying to signup with a user that has already tried to signup but has stopped in mobile number verification step
        NOTE: In this case everything should be ok and another verify code should be sent to user via sms
        """

        #providing the same credentials that we made an inactive user in setup of this test case
        req = {
            'username':'soheil', 
            'password':"simplepass2",
            'mobile':"093094328060",
            'email':"sohei@gmail.com",
            "is_real": True,
        }

        url = '/user/signup/'

        self.client = APIClient()
        respone = self.client.post(url, req)
        self.assertEqual(respone.data.get("succeeded"), True)
        self.assertEqual(respone.status_code, 200)


    def test_successful_signup(self):
        """this is the case that everything is ok and user should get an ok and sent to mobile verification step"""

        #totally ok and unique credentials provided by user.
        req = {
            "password": "simplepass",
            "mobile": "09052222222",
            "email": "soheildsh1@gmail.com",
            "is_real": True
        }

        url = '/user/signup/'
        self.client = APIClient()

        response = self.client.post(url, req)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("succeeded"), True)
        self.assertFalse(UserProfile.objects.filter(mobile="09052222222").first().is_active)








