# Generated by Django 4.0.2 on 2022-09-18 06:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('developinglogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receivedsms',
            name='sender_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
