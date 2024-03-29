# Generated by Django 4.0.2 on 2022-05-28 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        # ('accesslevel', '0005_userrowcountaccess_user'),
        ('user', '0002_user_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='common_access_level',
            field=models.ForeignKey(blank=True, help_text='سطح دسترسی متداولی که کاربر به آن دسترسی دارد', null=True, on_delete=django.db.models.deletion.SET_NULL, to='accesslevel.commonaccesslevel'),
        ),
    ]
