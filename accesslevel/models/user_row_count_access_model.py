from django.db import models
from user.models import UserProfile
from extra_scripts.timestampmodel import TimeStampedModel
from accesslevel.models import (
    CommonAccessLevel, )


class UserRowCountAccess(TimeStampedModel):
    """this modes is created for limiting user for reaching number of objects from a model based on their common_access_level 
    in each required views when setting query for list of a model , apply this after query"""
    title = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, blank=True, null=True, help_text='if we want this limit for spedific user')
    role = models.ForeignKey(
        CommonAccessLevel, on_delete=models.CASCADE, blank=True, null=True)
    model_name = models.CharField(
        max_length=100, blank=True, null=True,  help_text='name of the model we want limit for user')
    count_of_row = models.IntegerField(
        blank=True, null=True, help_text='number of objects user can access in list')
