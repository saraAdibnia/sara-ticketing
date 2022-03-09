# In this TestCase we are trying to manage user's profile
# retreiving and manuplating data are aimed to test here.
from rest_framework.test import APIClient, APITestCase

from datetime import datetime, date

from user.models import UserProfile
from user.tests.test_media import *
from places.models import City, State, Country


class ProfileCase(APITestCase):


    def setUp(self):
        """we create a user with fields shown below, in order to check the login proccess"""
        self.user1 = UserProfile.objects.create_user(
                                            password="thisisasimplepassword",
                                            mobile="09125351125",
                                            fname="سهیل",
                                            ename='soheil',
                                            flname='درویشی',
                                            elname='darvishi',
                                            uni_code='0012131231',
                                            email='soheildsh@gmail.com',
                                            city=City.objects.first(),
                                            state=State.objects.first(),
                                            country=Country.objects.first(),
                                            disposable_login=True,
                                            needs_to_change_pass=True,
                                            is_active=True,
                                            is_staff=False,
                                            role='0',
                                            birthday='1996-10-23'
                                        )

        # self.country = Country.objects.create(

        # )

        # self.state = State.objects.create(

        # )
        
        # self.city = City.objects.create(

        # )

    def test_profile_show(self):
        #loging in the user
        url = '/user/login/'
        self.client = APIClient()

        req = {
            'username': '09125351125',
            'password': 'thisisasimplepassword'
        }

        response = self.client.post(url, req)
        
        #trying to retreive user's data via get method using authorization that we got in login above, in header.
        url2 = '/user/profile/'
        self.client.credentials(HTTP_AUTHORIZATION=response.data.get("Authorization"))
        #get method of this root is to retreive data of profile
        response = self.client.get(url2)        

        #checking that every field are retreived as they were created and saved in setup of testcase
        self.assertEqual(response.data.get("user").get("mobile"), "09125351125")
        self.assertEqual(response.data.get("user").get("fname"), "سهیل")
        self.assertEqual(response.data.get("user").get("ename"), 'soheil')
        self.assertEqual(response.data.get("user").get("flname"), "درویشی")
        self.assertEqual(response.data.get("user").get("elname"), 'darvishi')
        self.assertEqual(response.data.get("user").get("uni_code"), '0012131231')
        self.assertEqual(response.data.get("user").get("email"), 'soheildsh@gmail.com')
        # self.assertEqual(response.data.get("user").get("city"), City.objects.first())


        # self.assertEqual(response.data.get("user").get("state"), State.objects.first())


        # self.assertEqual(response.data.get("user").get("country"), Country.objects.first())


        self.assertTrue(response.data.get("user").get("needs_to_change_pass"))
        self.assertEqual(response.data.get("user").get("role"), 0)
        self.assertEqual(response.data.get('user').get('birthday'), '1996-10-23')

    # def test_profile_edit(self):

    #     #trying to login the user to retreive their token to use in our profile request
    #     url = '/user/login/'
    #     self.client = APIClient()
    #     req = {
    #         'username': '09125351125',
    #         'password': 'thisisasimplepassword'
    #     }
    #     response = self.client.post(url, req)

    #     time = datetime.timestamp(datetime.now())   #used for user birthday


    #     req2 = {
    #         "mobile": "09309432860",
    #         "password": "newpass",
    #         "fname": "سهی",
    #         "ename": 'sohei',
    #         "flname": 'دروی',
    #         "elname": "darvi",
    #         "uni_code": "12121212",
    #         "email": "soheil@gmail.com",
    #         "disposable_login": False,
    #         "birthday": time,

    #         #these five should not change to these values, because they are not controlled by user. even if they are sent to api via request
    #         "temp_password": "11",
    #         "needs_to_change_pass": False,
    #         "is_active": False,
    #         "is_staff": True,
    #         "role": "1"
    #     }


    #     url2 = '/user/profile'
    #     #using user authorization credentials that we got in login above
    #     self.client.credentials(HTTP_AUTHORIZATION=response.data.get("Authorization"))

    #     #post method of this root is to manipulate and changing the data in user profile
    #     response2 = self.client.post(url2, req2)

    #     user_obj = UserProfile.objects.first()
    #     #these fields should have been updated
    #     self.assertEqual(user_obj.mobile, "09309432860")
    #     self.assertEqual(user_obj.fname, "سهی")
    #     self.assertEqual(user_obj.ename, "sohei")
    #     self.assertEqual(user_obj.flname, 'دروی')
    #     self.assertEqual(user_obj.elname, 'darvi')
    #     self.assertEqual(user_obj.uni_code, "12121212")
    #     self.assertEqual(user_obj.email, "soheil@gmail.com")
    #     self.assertFalse(user_obj.disposable_login)

    #     #these fields should have not be changed from what they were when we created user
    #     # self.assertTrue(user_obj.needs_to_change_pass)
    #     self.assertTrue(user_obj.is_active)
    #     self.assertFalse(user_obj.is_staff)
    #     self.assertEqual(user_obj.role, "0")
    #     self.assertEqual(user_obj.birthday, time)

    # def test_profile_picture_upload(self):
    #     """we are trying to upload profile image in this test"""
    #     #trying to get authorization credentials for user via login api
    #     url = '/user/login/'
    #     self.client = APIClient()
    #     req = {
    #         'username': '09125351125',
    #         'password': 'thisisasimplepassword'
    #     }
    #     response = self.client.post(url, req)
        

    #     #using test image located in the root address mentioned below as a sample profile image
    #     with open('./user/tests/test_media/1.png') as img:
    #         req2 = {
    #             "profile image": img.read
    #         }
    #         url2 = '/user/profile'
    #         #using authorization credentials of user in request header
    #         self.client.credentials(HTTP_AUTHORIZATION=response.data.get("Authorization"))
    #         #patch method of this root is for uploading user image
    #         response2 = self.client.patch(url2, req2)
            
    #         self.assertTrue(response2.data.get('succeeded'))
    #         self.assertEqual(response2.status_code, 200)
    #         self.assertNotEqual(UserProfile.objects.first().profile_image, None)


    def test_profile_picture_delete(self):
        """user can delete their profile image"""
        #trying to get authorization credentials for user via login api
        url = '/user/login/'
        self.client = APIClient()
        req = {
            'username': '09125351125',
            'password': 'thisisasimplepassword'
        }
        response = self.client.post(url, req)



        url2 = '/user/profile/'
        #using authorization credentials of user in request header
        self.client.credentials(HTTP_AUTHORIZATION=response.data.get("Authorization"))
        #delete method of mentioned url is to delete user profile image
        response2 = self.client.delete(url2)

        self.assertFalse(UserProfile.objects.filter(mobile='09125351125').first().profile_image)