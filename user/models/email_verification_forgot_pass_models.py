from django.db import models



class EVFP(models.Model):
    '''
    EVFP: email verification and forgot password
    '''
    user = models.ForeignKey(
        'user.UserProfile',
       on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text='',
    )

    code = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        unique=True,
        help_text='',
    )
