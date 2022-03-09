# Generated by Django 3.2.5 on 2021-09-08 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0002_auto_20210531_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_log',
            name='log_kind',
            field=models.SmallIntegerField(choices=[(0, 'ورود کاربر'), (1, 'رمز اشتباه'), (2, 'خروج کاربر')], default=0, help_text='نوع لاگ'),
        ),
    ]
