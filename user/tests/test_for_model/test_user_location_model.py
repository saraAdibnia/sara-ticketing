##this test is to evaluate object creation in userlocation model
from rest_framework.test import APIClient, APITestCase

from user.models import UserProfile, UserLocation, UserBankAccount, LegalUserInfo
from places.models import Country, City, State
from django.contrib.gis.geos import Point

from datetime import datetime

class UserModelCase(APITestCase):

    def setUp(self):
        """we try to create a user_location object"""
        #first we create a user
        user1 = UserProfile.objects.create_user(
            mobile='09125351125', 
            password='simplepass', 
            # temp_password='1234'
            )

        #making a point for user location model
        self.point = Point(38.670049, -99.565798)

        #creatting user_location object
        user_location = UserLocation.objects.create(
            user=UserProfile.objects.first(),
            country = Country.objects.first(),
            city = City.objects.first(),
            state = State.objects.first(),
            address_name = 'شرکت',
            full_name='سپهر محمدی',
            uni_code='12123131',
            mobile='0912324324',
            address_text = 'خیابان قنبر زاده - نبش برزی - آسمان سوی پارسیان',
            phone = '02145312',
            postal_code = '12121212',
            location = self.point,
            description = 'این لوکیشن آدرس محل کار من است.',
            default = True,  
            )


    def test_model(self):
        #retreiving the user and user_location object
        user_obj = UserProfile.objects.first()
        user_location_obj = UserLocation.objects.first()

        #checking every field to 
        self.assertEqual(UserProfile.objects.first(), user_location_obj.user)
        self.assertEqual(user_location_obj.address_name, 'شرکت')
        self.assertEqual(user_location_obj.full_name, 'سپهر محمدی')
        self.assertEqual(user_location_obj.uni_code, '12123131')
        self.assertEqual(user_location_obj.mobile, '0912324324')
        self.assertEqual(user_location_obj.address_text, 'خیابان قنبر زاده - نبش برزی - آسمان سوی پارسیان')
        self.assertEqual(user_location_obj.phone, '02145312')
        self.assertEqual(user_location_obj.postal_code, '12121212')
        self.assertEqual(user_location_obj.description, 'این لوکیشن آدرس محل کار من است.')
        self.assertTrue(user_location_obj.default)
        self.assertFalse(user_location_obj.hidden)
        self.assertEqual(user_location_obj.location, self.point)
