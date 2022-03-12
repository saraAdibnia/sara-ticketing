from django.db import models
from django.conf import settings
from django.dispatch import receiver
from user.models import UserProfile
from department.models import Department     

class Tag(models.Model):
    e_name = models.CharField(max_length=30 ,null = True , blank = True)
    f_name = models.CharField(max_length=30 ,null = True , blank = True)

class Category(models.Model):
    name = models.CharField(max_length=200  , blank=True, null=True)  
    parent = models.ForeignKey('Category' , blank=True, null=True , on_delete=models.CASCADE)

class Ticket(models.Model):
    title = models.TextField(max_length=100 , null = True , blank = True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE , related_name='Department_department' , blank = True , null = True )
    user= models.ForeignKey(UserProfile,  on_delete=models.CASCADE, related_name='user_id',null = True , blank = True ,
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

class Answer(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE ,null = True , blank = True)
    text=models.CharField(max_length=300 , null = True , blank = True)
    user= models.ForeignKey(UserProfile,  on_delete=models.CASCADE , null = True , blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)
    to_operator = models.CharField(max_length=30 , null = True , blank = True)
    to_department = models.CharField(max_length=30 , null = True , blank = True)

class File(models.Model):
    name = models.CharField(max_length=30 ,null = True , blank = True)
    file_field = models.FileField(null = True , blank = True , upload_to="MEDIA/")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)
    ticket = models.ForeignKey(Ticket , null = True , blank = True , on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer , null = True , blank = True , on_delete=models.CASCADE)
    

    




