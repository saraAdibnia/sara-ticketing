from django.db import models
from django.conf import settings
from django.dispatch import receiver
from user.models import UserProfile
     

class Department(models.Model):
    name = models.CharField(max_length=30 , null = True , blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)



class Tag(models.Model):
    e_name = models.CharField(max_length=30 ,null = True , blank = True)
    f_name = models.CharField(max_length=30 ,null = True , blank = True)



class Ticket(models.Model):
    title = models.TextField(max_length=100 , null = True , blank = True)
    department = models.ForeignKey(UserProfile, on_delete=models.CASCADE , related_name='department_system' , blank = True , null = True )
    user= models.ForeignKey(UserProfile,  on_delete=models.CASCADE, related_name='user_id',
                                    verbose_name='user_id' ,  help_text='The owner of ticket either for themself or customers or co-workers')
    operator = models.ForeignKey(UserProfile,null = True, on_delete=models.CASCADE, blank = True , related_name='operator' , help_text = 'whom the user sends the ticket to')
    created_by = models.ForeignKey(UserProfile,null = True, on_delete=models.CASCADE ,blank = True ,  help_text = 'who sends the request for creating the ticket')
    text=models.TextField(max_length=300 , null = True , blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank = True)
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
    # user= models.ForeignKey(UserProfile,  on_delete=models.CASCADE , null = True , blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)

class Category(models.Model):
    name = models.CharField(max_length=200  , blank=True, null=True)  
    parent = models.ForeignKey('self',blank=True, null=True , on_delete=models.CASCADE)





