from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework import serializers


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#         if created:
#             print(Token.objects.create(user=instance))
         




class Department(models.Model):
    name = models.CharField(max_length=30 , null = True , blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)


class UserProfile(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE , null = True , blank = True) 
    mobile = models.CharField(max_length=11 , null = True , blank = True) #for example 09123456789
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True , blank = True)


class Ticket(models.Model):
    subject = models.CharField(max_length=100 , null = True , blank = True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE , blank = True , null = True )
    user= models.ForeignKey(User,  on_delete=models.CASCADE, related_name='user_id',
                                    verbose_name='user_id' , blank = True , null = True)
    operator = models.ForeignKey(User,null = True, on_delete=models.CASCADE, related_name='operator',

                                    verbose_name='operator', blank = True)
    text=models.TextField(max_length=300 , null = True , blank = True)
    is_answered = models.BooleanField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)



class File(models.Model):
    name = models.CharField(max_length=30 ,null = True , blank = True)
    # path = models.CharField(max_length=100 , null = True , blank = True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE ,null = True ,blank = True)
    user= models.ForeignKey(User,  on_delete=models.CASCADE , null = True , blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)


class Answer(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE ,null = True , blank = True)
    text=models.CharField(max_length=300 , null = True , blank = True)
    user= models.ForeignKey(User,  on_delete=models.CASCADE , null = True , blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)
    



