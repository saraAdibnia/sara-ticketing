from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager

class UserProfileManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, mobile, password, **extra_fields):
        if not mobile:
            raise ValueError('The given mobile must be set')
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile, password, **extra_fields)

    def create_superuser(self, mobile, password, **extra_fields):
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
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    department = models.ForeignKey("System.Department",related_name='department_userProfile' , null = True , blank = True ,on_delete=models.CASCADE)
    username = None
    objects = UserProfileManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []
