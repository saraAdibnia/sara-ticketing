from django.db import models
from user.models import User
class Department(models.Model):
    ename = models.CharField(max_length=30 , null = True , blank = True)
    fname = models.CharField(max_length=30 , null = True , blank = True)
    created = models.DateTimeField(auto_now_add=True)
    modified =models.DateTimeField(auto_now=True)
    admin = models.ForeignKey(User,null = True, on_delete=models.CASCADE, blank = True , related_name='department_admin' , help_text = 'admin of the department')
    deleted = models.BooleanField(default=False, blank=True, null=True)
