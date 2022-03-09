from rest_framework.test import APIClient, APITestCase

from user.models import UserProfile, LegalUserInfo
from places.models import City, State, Country
from datetime import datetime, date


class LegalUserInfoTestCase(APITestCase):

    def setUp(self):
        user = UserProfile.objects.create(
            mobile='09125351125',
            password='password'
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

        legaluserinfo = LegalUserInfo.objects.create(
            company_name='اسم شرکت',
            economic_code='123132',
            national_id='12312312',
            registration_id='123123',
            register_date='2020-12-22',
            postal_code='213132131321',
            phone='021312313',
            address_text='خیابان بهشتی',
            field_of_work='داروسازی',
            email='soheildsh@gmail.com',
            city=City.objects.first(),
            state=State.objects.first(),
            country=Country.objects.first()
        )

        self.now = datetime.timestamp(datetime.now())

    def test_legal_instance_creation(self):
        legal_user_info_obj = LegalUserInfo.objects.first()
        self.assertEqual(legal_user_info_obj.company_name ,'اسم شرکت')
        self.assertEqual(legal_user_info_obj.economic_code ,'123132')
        self.assertEqual(legal_user_info_obj.national_id ,'12312312')
        self.assertEqual(legal_user_info_obj.registration_id ,'123123')
        self.assertEqual(legal_user_info_obj.postal_code, '213132131321')
        self.assertEqual(legal_user_info_obj.address_text, 'خیابان بهشتی')
        self.assertEqual(legal_user_info_obj.register_date ,date(2020,12,22))
        self.assertEqual(legal_user_info_obj.phone ,'021312313')
        self.assertEqual(legal_user_info_obj.field_of_work ,'داروسازی')
        self.assertEqual(legal_user_info_obj.email , 'soheildsh@gmail.com')
        self.assertEqual(legal_user_info_obj.city , City.objects.first())
        self.assertEqual(legal_user_info_obj.state ,State.objects.first())
        self.assertEqual(legal_user_info_obj.country ,Country.objects.first())
        # self.assertLessEqual(self.now-legal_user_info_obj.created, 10)
        # self.assertLessEqual(self.now-legal_user_info_obj.last_update, 10)

