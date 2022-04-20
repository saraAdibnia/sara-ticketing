# Generated by Django 4.0.2 on 2022-04-20 08:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accesslevel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesslevelrequest',
            name='user',
            field=models.ForeignKey(blank=True, help_text='دسترسی برای چه کاربری درخواست شده؟', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='access_level_request_user', to=settings.AUTH_USER_MODEL),
        ),
    ]