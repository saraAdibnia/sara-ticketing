from django.forms import CharField


from django.db import models

class Question(models.Models):
    text = CharField(max_length=100 , null = True , blank = True)
class Answer(models.Models):
    text = CharField(max_length=300 , null = True , blank = True)