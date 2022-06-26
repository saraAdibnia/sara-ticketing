from django.db import models
from extra_scripts.timestampmodel import TimeStampedModel  

class FrequentlyAskedQuestion(TimeStampedModel):
    title =  models.CharField(max_length=100, null = True , blank = True)
    text = models.CharField(max_length=300 , null = True , blank = True)
    description = models.CharField(max_length = 1000 , null = True , blank = True)