from tkinter import CASCADE
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from psycopg2 import Timestamp
from user.models import User
from department.models import Department
from extra_scripts.timestampmodel import TimeStampedModel     
from System.formatChecker import ContentTypeRestrictedFileField
from django.core.validators import MaxValueValidator, MinValueValidator
class Tag(TimeStampedModel):
    """ 
     various tags for tickets 

    """
    ename = models.CharField(max_length=30 ,null = True , blank = True)
    fname = models.CharField(max_length=30 ,null = True , blank = True)

class Category(TimeStampedModel):
    """
     various categories for tickets

    """
    ename = models.CharField(max_length=200  , blank=True, null=True)
    fname = models.CharField(max_length=200  , blank=True, null=True)  
    parent = models.ForeignKey('Category' , blank=True, null=True , on_delete=models.CASCADE)




class Ticket(TimeStampedModel):
    """
     model of tickets

    """
    title = models.TextField(max_length=100 , null = True , blank = True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE , related_name='department_department' , blank = True , null = True )
    user= models.ForeignKey(User,  on_delete=models.CASCADE, related_name='user_id',null = True , blank = True ,
                                    verbose_name='user_id' ,  help_text='The owner of ticket either for themself or customers or co-workers')

    operator = models.ForeignKey(User,null = True, on_delete=models.CASCADE, blank = True , related_name='operator' , help_text = 'whom the user sends the ticket to')
    created_by = models.ForeignKey(User,null = True, on_delete=models.CASCADE ,blank = True ,  help_text = 'who sends the request for creating the ticket')
    text=models.TextField(max_length=300 , null = True , blank = True)
    tags = models.ManyToManyField(Tag, blank = True)
    is_answered = models.BooleanField(default = False )
    STATUS_CHOICES = [
    (0, 'baste'),
    (1, 'jari'),
    (2, 'baz'),
    (3, 'is_suspended'),
    ]
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=2,
    )
    KIND_CHOICES = [
    (1, 'internal organizational'),
    (2, 'extra organizational'),
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
    category = models.ForeignKey(Category,null = True, on_delete=models.CASCADE, blank = True )
    sub_category =models.ForeignKey(Category,related_name="sub_categories" , null = True, on_delete=models.CASCADE, blank = True )
    deleted = models.BooleanField(default=False, blank=True, null=True)
class Answer(TimeStampedModel):
    """
    model for answer of tickets

    """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE ,null = True , blank = True)
    text=models.CharField(max_length=300 , null = True , blank = True)
    sender= models.ForeignKey(User,  on_delete=models.CASCADE , null = True , blank = True)
    reciever = models.ForeignKey(User, null = True , blank = True,related_name= 'recivers' , on_delete=models.CASCADE)
    to_department = models.ForeignKey(Department , null = True , blank = True ,  on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False, blank=True, null=True)
    REACTION_CHOICES = [
    (0, 'Thumbs Down'),
    (1, 'Thmbs Up '),
    (2, 'Thinking Face'),
    (3, 'Red Heart'),
    ]
    reaction = models.IntegerField( null = True , 
        choices= REACTION_CHOICES, )
class File(TimeStampedModel):
    """
     file to attach to answer or ticket

    """
    name = models.CharField(max_length=250 ,null = True , blank = True)
    file= ContentTypeRestrictedFileField( upload_to="MEDIA/", content_types=['video/x-msvideo', 'application/pdf', 'video/mp4', 'audio/mpeg', ],max_upload_size=5242880,blank=True, null=True)
    ticket = models.ForeignKey(Ticket , null = True , blank = True , on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer , null = True , blank = True , on_delete=models.CASCADE)
    url = models.CharField(max_length=250 ,null = True , blank = True)
class waybill(models.Model):
    """
     waybills

    """
    code =models.CharField(max_length=30 ,null = True , blank = True)
    waybill_id = models.IntegerField(null = True , blank = True)

class Review(TimeStampedModel):
    """
        to rate and leave comments for every ticket after closing it 
    """
    rating = models.SmallIntegerField(default = 5 , validators =[MaxValueValidator(5) , MinValueValidator(1) ] )
    comment = models.CharField(max_length= 500 , blank = True , null = True)
    user = models.ForeignKey(User ,  null = True , blank = True ,on_delete= models.CASCADE)
    ticket = models.ForeignKey(Ticket , null= True , blank = True , on_delete = models.CASCADE)