
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime, timedelta
from rest_framework import exceptions
import pytz
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.db import models
# TODO doc
from rest_framework.authentication import TokenAuthentication
from django.conf import settings
import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='myauth_token',
        on_delete=models.CASCADE, verbose_name=_("User"),blank = True, null = True
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, blank= True ,null= True)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        print("creatng my token \n\n")
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key






class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = MyToken.objects.get(key=key)
    
            print(f'**************************************\n')
        except MyToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')
        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)
        if not token.modified or token.modified < utc_now - timedelta(hours=2):
            raise exceptions.AuthenticationFailed(
                'به علت کار نکردن با سیستم احراز هویت شما نا معتبر است لطفا دوباره وارد شوید')
        if token.created < utc_now - timedelta(hours=9):
            raise exceptions.AuthenticationFailed(
                'احراز هویت شما منقضی شده است دوباره وارد شوید')
        token.modified = datetime.utcnow()
        token.save()

        return token.user, token

