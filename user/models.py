from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager


class UserProfileManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, mobile, password, **extra_fields):
        if not mobile:
            raise ValueError('The given mobile must be set')
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile, password, **extra_fields)

    def create_superuser(self, mobile, password, **extra_fields):
        if password is None:
            raise TypeError('Superusers must have a password.')
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        user=self._create_user(mobile, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class UserProfile(AbstractUser):
    mobile = models.CharField( max_length=11 , null = True , blank = True , unique= True) #for example 09123456789
    first_name = models.CharField(max_length=30,null = True , blank=True)
    last_name = models.CharField(max_length=30,null = True , blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    department = models.ForeignKey("System.Department",related_name='department_userProfile' , null = True , blank = True ,on_delete=models.CASCADE)
    ROLE_CHOICES = [
    (0, 'modir amel'),
    (1, 'modir mali'),
    ]
    role = models.SmallIntegerField(
        choices=ROLE_CHOICES,
        default=2,
    )
    username = None
    created_by = models.CharField(max_length=30,null = True , blank=True)
    objects = UserProfileManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

