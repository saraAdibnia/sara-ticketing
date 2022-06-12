from django.db import models


def captcha_save_path(instance, filename):
    return 'captcha/{}.{}'.format(instance.id, filename)

class Captcha(models.Model):

    created_date = models.DateTimeField(auto_now_add=True)

    modified_date =models.DateTimeField(auto_now=True)

    captcha = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text=''
    )

    code = models.CharField(
        blank=True,
        null=True,
        max_length=10,
        help_text='captcha code'
    )

