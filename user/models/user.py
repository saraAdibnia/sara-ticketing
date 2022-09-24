from sre_parse import State
from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from user.abstract import AbstractBaseUser
from django.core.exceptions import ValidationError
import uuid
from datetime import datetime
from PIL import Image
from places.models import Country, DialCode, State
from simple_history.models import HistoricalRecords

def user_ProfileImage_directory_path(instance, filename):
    return './users/user_{0}/ProfileImage/{1}'.format(instance.id, filename)


def user_File_directory_path(instance, filename):
    return './users/user_{0}/File/{1}'.format(instance.user.id, filename)


def Validate_Image(image):
    ImageSize = image.size
    megabyte_limit = 1
    if ImageSize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


class UserManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, mobile, role=0, password=None, temp_password=None, **extra_fields):
        """create a new user profile"""

        user = self.model(mobile=mobile, role=role, **extra_fields)

        user.set_password(password)
        user.set_temppassword(temp_password)
        user.save()

        return user

    def create_superuser(self, mobile, password, role="3", **extra_fields):
        """create and save a new superuser with given details"""
        user = self.create_user(mobile=mobile, role="3",
                                password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Database Model for users in the system"""

    username = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        unique=True,
    )

    history = HistoricalRecords()

    mobile = models.CharField(
        max_length=20,
        blank=False,
        unique=True,
        help_text='شماره موبایل (فیلد اصلی یوزرنیم)',
    )

    fname = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text='اسم کوچک فارسی',
    )

    ename = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='اسم کوچک انگلیسی',
    )

    flname = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text='نام خانوادگی فارسی',
    )

    elname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='نام خانوادگی انگلیسی',
    )

    economic_code = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        help_text='کد اقتصادی (حقوقی)',
    )

    national_id = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        help_text='شناسه ملی (حقوقی)',
    )

    registration_id = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        help_text='شناسه ثبت (حقوقی)'
    )

    register_date = models.DateField(
        blank=True,
        null=True,
        help_text='تاریخ ثبت (حقوقی)',
    )

    postal_code = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        help_text='کد پستی (حقوقی)'
    )

    address_text = models.CharField(
        blank=True,
        null=True,
        max_length=1500,
        help_text='آدرس شرکت (حقوقی)'
    )

    phone = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        help_text='شماره تلفن ثابت',
    )

    field_of_work = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        help_text='حوزه‌ی کاری (حقوقی)',
    )

    uni_code = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='کد ملی',
    )

    email = models.EmailField(
        blank=True,
        null=True,
        help_text='ایمیل'
    )

    email_verified = models.BooleanField(
        default=False,
        help_text='ایا ایمیل اعتبارسنجی شده یا خیر',
    )

    birthday = models.DateField(
        blank=True,
        null=True,
        help_text='تاریخ تولد (حقیقی)',
    )

    profile_image = models.ImageField(
        blank=True,
        null=True,
        upload_to=user_ProfileImage_directory_path,
        validators=[Validate_Image],
        help_text='عکس پروفایل',
    )

    department = models.ForeignKey(
        "department.Department", related_name='department_User', blank=True, null=True, on_delete=models.CASCADE)

    needs_to_change_pass = models.BooleanField(
        default=False,
        help_text='آیا یوزر از فراموشی رمز عبور استفاده کرده و مجبور است رمز خود را عوض کند؟',
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False
    )

    banned = models.BooleanField(
        default=False,
        help_text='یوزر از سایت بن شده'
    )

    ban_cause = models.TextField(
        blank=True,
        null=True,
        help_text='علت بن شدن یوزر از سایت'
    )

    banned_by = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='user_banned_by',
        help_text='یوزر توسط چه کسی بن شده'
    )

    is_real = models.BooleanField(
        default=True,
        help_text='یوزر حقیقی‌ است یا حقوقی'
    )

    role_choices = (
        (0, "کاربر عادی"),
        (1, "کاربر داشبورد سازمانی"),
        (2, "تحصیل‌دار"),
        (3 , "ادمین"),
        (4 , "ادمین دپارتمان")
    )

    role = models.SmallIntegerField(
        default=0,
        choices=role_choices,
        help_text='handling the user kind, role'
    )

    confirmation_choices = (
        (0, "not valid"),
        (1, "valid"),
        (2, "signed up"),   
    )

    confirmation = models.SmallIntegerField(
        default=0,
        choices=confirmation_choices,
        help_text='validation status for signup'
    )

    common_access_level = models.ForeignKey(
        'accesslevel.CommonAccessLevel',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='سطح دسترسی متداولی که کاربر به آن دسترسی دارد',
    )

    access_granted_by = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='user_access_granted_by',
        help_text='دسترسی به این کاربر آخرین بار توسط چه کسی داده شده است.',
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='کشور محل سکونت',
        default=1112,
    )
    state = models.ForeignKey(
        State,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='استان محل سکونت',
        default=19395,
    )
    dial_code = models.ForeignKey(
        DialCode,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='',
    )
    signiture = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='امضا',
    )
    # rated = models.BooleanField(default=False, blank=True, null=True)
    gender = models.BooleanField(
        blank=True, null=True, help_text="male = True, female = False")

    created_time = models.DateTimeField(auto_now_add=True)

    modified = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)
    # this part is canceled
    direct_login = models.BooleanField(default=False, null=True, blank=True)
    # history = HistoricalRecords()

    # specifing class for objects attribute of this class
    objects = UserManager()

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return (str(self.fname) or "") + ' ' + (str(self.flname) or "") + ' ' + str(self.mobile)

    def save(self, *args, **kwargs):
        super().save()
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            if img.height > 100 or img.width > 100:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_image.path)
        # if not self.country:
        #     self.country = self.country_initials()


class UserFiles(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User,
                             null=True, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_File_directory_path,
                            blank=True, null=True, help_text="corportate user files")
    created_time = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    modified_time = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    deleted = models.BooleanField(default=False, blank=True, null=True)
