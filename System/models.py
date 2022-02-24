from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import PasswordInput
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import AbstractUser , BaseUserManager


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#         if created:
#             print(Token.objects.create(user=instance))
         




class Department(models.Model):
    name = models.CharField(max_length=30 , null = True , blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)

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

        return self._create_user(mobile, password, **extra_fields)

class UserProfile(AbstractUser):
    mobile = models.CharField( max_length=11 , null = True , blank = True , unique= True) #for example 09123456789
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
 
    objects = UserProfileManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

class Tag(models.Model):
    e_name = models.CharField(max_length=30 ,null = True , blank = True)
    f_name = models.CharField(max_length=30 ,null = True , blank = True)



class Ticket(models.Model):
    title = models.TextField(max_length=100 , null = True , blank = True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE , blank = True , null = True )
    user= models.ForeignKey(UserProfile,  on_delete=models.CASCADE, related_name='user_id',
                                    verbose_name='user_id' , blank = True , null = True ,  help_text='The owner of ticket either for themself or customers or co-workers')
    operator = models.ForeignKey(UserProfile,null = True, on_delete=models.CASCADE, blank = True , related_name='operator' , help_text = 'whom the user sends the ticket to')
    created_by = models.ForeignKey(UserProfile,null = True, on_delete=models.CASCADE ,blank = True ,  help_text = 'who sends the request for creating the ticket')
    text=models.TextField(max_length=300 , null = True , blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    is_answered = models.BooleanField(default = False )
    STATUS_CHOICES = [
    (0, 'baste'),
    (1, 'jari'),
    (2, 'baz'),
    ]
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=2,
    )
    KIND_CHOICES = [
    (1, 'DARUN SAZMANI'),
    (2, 'BIRUN SAZMANI'),
    ]
    kind = models.IntegerField(
        choices=KIND_CHOICES,
        default=1,
    )
    PRIORITY_CHOICES = [
    (0, 'LOW'),
    (1, 'MIDDLE'),
    (2, 'HIGH'),
    ]
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=0,
    )


class File(models.Model):
    name = models.CharField(max_length=30 ,null = True , blank = True)
    file_field = models.FileField(null = True , blank = True , upload_to="media/")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)
    ticket = models.ForeignKey(Ticket , null = True , blank = True , on_delete=models.CASCADE)

class Answer(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE ,null = True , blank = True)
    text=models.CharField(max_length=300 , null = True , blank = True)
    user= models.ForeignKey(UserProfile,  on_delete=models.CASCADE , null = True , blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)

class Category(models.Model):
    name = models.CharField(max_length=200  , blank=True, null=True)  
    parent = models.ForeignKey('self',blank=True, null=True , on_delete=models.CASCADE)





