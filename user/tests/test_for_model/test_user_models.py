# in this test we are going to check wether the attributes of our user model objects,
#  will be saved properly or not
from rest_framework.test import APIClient, APITestCase

from user.models import UserProfile
from user.serializers import *
from places.models import City, State, Country


class UserModelCase(APITestCase):

    def setUp(self):

        country = Country.objects.create(
            ename='Iran'
        )
        state = State.objects.create(
            ename='Tehran'
        )
        city = City.objects.create(
            ename="Tehran"
        )

        #creating the user
        user = UserProfile.objects.create_user(
            mobile='09125351125',
            fname='سهیل',
            ename='soheil',
            flname='درویشی',
            elname='darvishi',
            uni_code='00164464654646',
            email='soheildsh@gmail.com',
            city=City.objects.first(),
            state=State.objects.first(),
            country=Country.objects.first(),
        )

    def test_usercreation(self):
        """we check to see if every field is saved right"""

        user_obj = UserProfile.objects.first()
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(user_obj.mobile, '09125351125')
        self.assertEqual(user_obj.fname, 'سهیل')
        self.assertEqual(user_obj.ename, 'soheil')
        self.assertEqual(user_obj.flname, 'درویشی')
        self.assertEqual(user_obj.elname, 'darvishi')
        self.assertEqual(user_obj.uni_code, '00164464654646')
        self.assertEqual(user_obj.email, 'soheildsh@gmail.com')
        self.assertEqual(user_obj.city, City.objects.first())
        self.assertEqual(user_obj.state, State.objects.first())
        self.assertEqual(user_obj.country, Country.objects.first())
