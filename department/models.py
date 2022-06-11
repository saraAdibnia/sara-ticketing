from django.db import models

class Department(models.Model):
    ename = models.CharField(max_length=30 , null = True , blank = True)
    fname = models.CharField(max_length=30 , null = True , blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, blank=True, null=True)
